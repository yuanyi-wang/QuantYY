# -*-coding:utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import akshare as ak
from loguru import logger

import common.supports as supports
import common.constants as cs

from rejson import Client, Path

REDIS_CLIENT = Client(host=supports.APP_CONFIG["redis"]["host"], \
                        port=supports.APP_CONFIG["redis"]["port"], \
                            db=0, password=supports.APP_CONFIG["redis"]["password"], \
                                decode_responses=True)

@logger.catch()
def download_zh_stock_data():
    """
    下载沪深京A股实时数据
    """
    df_stock_zh = ak.stock_zh_a_spot_em()
    return df_stock_zh

@supports.func_execution_timer
@logger.catch
def save_current_zh_stock_price_data(price_big_change_warn):
    today_str = supports.today()
    now_str = supports.now()
    
    df_stock_zh = download_zh_stock_data()
    
    tasklist = []
    # 创建一个线程池, 最大线程数为 (系统 CPU 数 - 1)
    with ThreadPoolExecutor(max_workers=supports.CPU_COUNT - 1) as threadPool:
        for index, row in df_stock_zh.iterrows():
            logger.debug(f"Create thread task for {row['代码']} - {index}")
            task = threadPool.submit(_generate_min_price_data, row, today_str, \
                now_str, price_big_change_warn)
            tasklist.append(task)

    wait(tasklist, return_when=ALL_COMPLETED)
    tasklist.clear()

@logger.catch
def _generate_min_price_data(row, str_date, str_time, price_big_change_warn):
    """
    '序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', 
    '最高', '最低', '今开', '昨收', '量比', '换手率', '市盈率-动态', '市净率', '总市值', 
    '流通市值', '涨速', '5分钟涨跌', '60日涨跌幅', '年初至今涨跌幅'
    """
    
    if price_big_change_warn is not None:
        price_big_change_warn(row)
    
    stock_symbol = row["代码"]
    item = {
        cs.TIME: str_time,
        "price": supports.j(row['最新价'])
    }
    summary = {
        cs.DATE:                str_date,
        cs.STOCK_SYMBOL:        row['代码'],
        cs.STOCK_NAME:          row['名称'],
        cs.OPEN_PRICE:          supports.j(row['今开']),
        cs.HIGHEST_PRICE:       supports.j(row['最高']),
        cs.LOWEST_PRICE:        supports.j(row['最低']),
        cs.TRANSACTION_VOLUME:  supports.j(row['成交量']),
        cs.TRANSACTION_VALUE:   supports.j(row['成交额']),
        cs.TURNOVER_RATE:       supports.j(row['换手率']),
        cs.LATEST_PRICE:        supports.j(row['最新价'])
    }

    key = f"{stock_symbol}_{str_date}"
    
    def __generate_data_header(stock):
        stock["summary"] = summary

    def __generate_min_price_item(stock):
        if len(stock["prices"]) > 0 and stock["prices"][-1][cs.TIME] == str_time:
            return
        
        stock["prices"].append(item)

    stock = REDIS_CLIENT.jsonget(key)
    
    if stock is None:
        stock = {
            "summary": {},
            "prices": []
        }

    __generate_data_header(stock)
    __generate_min_price_item(stock)        
    
    REDIS_CLIENT.jsonset(name=key, path=Path.rootPath(), obj=stock)
