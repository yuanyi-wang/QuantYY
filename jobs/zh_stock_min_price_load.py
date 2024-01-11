# -*-coding:utf-8 -*-

import os
import pickle
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import json

import akshare as ak
from loguru import logger

import common.supports as supports
import common.send_wechat as wechat
from common.constants import * 

@logger.catch()
def get_data_file_name_path():
    formatted_time = supports.now().replace(":", "")
    file_name = f"stock_zh_{formatted_time}.pkl"
    data_folder_name = supports.get_today_data_path()
    if not data_folder_name.exists() :
        os.makedirs(data_folder_name)

    return data_folder_name / file_name


@logger.catch()
def download_and_save_zh_stock(data_file):
    df_stock_zh = ak.stock_zh_a_spot_em()
    
    with open(data_file, 'wb') as file:
        pickle.dump(df_stock_zh, file)
        logger.info(f'Object successfully saved to "{data_file}"')

    return df_stock_zh

@supports.func_execution_timer
@logger.catch
def generate_min_price_files(df_stock_zh, date_str, time_str):
    tasklist = []
    # 创建一个线程池, 最大线程数为 (系统 CPU 数 - 1)
    with ThreadPoolExecutor(max_workers=supports.CPU_COUNT - 1) as threadPool:
        for index, row in df_stock_zh.iterrows():

            stock_code = row['代码']

            if stock_code[0] != "6":
                continue

            logger.debug(f"Create thread task for {row['代码']}")
            task = threadPool.submit(_generate_min_price_file, row, date_str, time_str)
            tasklist.append(task)

    wait(tasklist, return_when=ALL_COMPLETED)
    tasklist.clear()


INTRESTING_SCTOCKS = {'601166':11000, '600036':43000, '000001':11300, '601890':3100,'600435':1000,'002049':100,'600973':300}

def _whether_sent_today(stock_symbol) -> bool:
    path_runtime = supports.PATH_DATA / "runtime"
    if not path_runtime.exists():
        path_runtime.mkdir()
    
    path_cfg_file = path_runtime / f"{supports.today()}.json"

    if path_cfg_file.exists():
        with open(path_cfg_file, "r") as f:
            json_data = json.load(f)
            sent_notifications = json_data.get("sent_notifications", [])
            return stock_symbol in sent_notifications
    else:
        with open(path_cfg_file, "w") as f:
            json_data = {'sent_notifications': []}
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return False

def _update_sent_today(stock_symbol):
    path_cfg_file = supports.PATH_DATA / "runtime" /  f"{supports.today()}.json"

    with open(path_cfg_file, "r") as f:
        json_data = json.load(f)
        sent_notifications_set = set(json_data.get("sent_notifications", []))
        sent_notifications_set.add(stock_symbol)
        json_data["sent_notifications"] = list(sent_notifications_set)
    with open(path_cfg_file, "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def _warn_(row):
    """
    价格有重大变动报警
    """
    stock_symbol = row["代码"]
    sotck_name = row['名称']
    if stock_symbol in INTRESTING_SCTOCKS.keys():
        if abs(row['5分钟涨跌']) > 3 or abs(row['涨跌幅']) > 5:
            if not _whether_sent_today():
                wechat.send_message(f"[{sotck_name}] 价格有重大变动", \
                    f"今开: {row['今开']}" + \
                    f"最高: {row['最高']}" + \
                    f"最低: {row['最低']}" + \
                    f"最新价: {row['最新价']}" + \
                    f"成交量: {row['成交量']}" + \
                    f"成交额: {row['成交额']}" + \
                    f"换手率: {row['换手率']}", 
                    url=f"https://quote.eastmoney.com/concept/sh{stock_symbol}.html")
            _update_sent_today(stock_symbol)


@logger.catch
def _generate_min_price_file(row, str_date, str_time):
    """
    '序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', 
    '最高', '最低', '今开', '昨收', '量比', '换手率', '市盈率-动态', '市净率', '总市值', 
    '流通市值', '涨速', '5分钟涨跌', '60日涨跌幅', '年初至今涨跌幅'
    """
    
    _warn_(row)
    

    stock_code = row["代码"]
    market_code = "SH"
    item = {
        TIME: str_time,
        LATEST_PRICE: row['最新价']
    }
    summary = {
        DATE: str_date,
        OPEN_PRICE: row['今开'],
        HIGHEST_PRICE: row['最高'],
        LOWEST_PRICE: row['最低'],
        TRANSACTION_VOLUME: row['成交量'],
        TRANSACTION_VALUE: row['成交额'],
        TURNOVER_RATE: row['换手率']
    }

    file_data_folder_path = supports.PATH_DATA / "zh_stocks" / market_code / stock_code

    if not file_data_folder_path.exists():
        os.makedirs(file_data_folder_path)
    
    file_full_path = file_data_folder_path / f"{str_date}.json"
    
    def __generate_file_header(stock):
        stock["summary"] = summary

    def __generate_min_price_item(stock):
        if len(stock["prices"]) > 0 and stock["prices"][-1][TIME] == str_time:
            return
        
        stock["prices"].append(item)


    if file_full_path.exists() and file_full_path.stat().st_size > 0:
        # existing file
        with open(file_full_path, "r") as f:
            stock = json.load(f)
            __generate_file_header(stock)
            __generate_min_price_item(stock)
    else:
        # new file
        stock = {
            "summary": {},
            "prices": []
        }
        __generate_file_header(stock)
        __generate_min_price_item(stock)
    
    with open(file_full_path, "w", encoding='utf-8') as f:
        json.dump(stock, f, ensure_ascii=False, indent=4)


def insert_data_to_db(df_stock_zh):

    # import pymysql

    # conn = pymysql.connect(host="192.168.3.6", port=3306, user='root', 
    #                        passwd='Qiqi0202', db='quantyy', charset='utf8mb4')
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # sql = "insert into USER (date, time, stock_code, price, quote_change, " + \
    # "changes, volume, turnover, amplitude, highest, lowest, quantity_ratio, " + \
    # "turnover_rate, dynamic_price_earning_ratio , change_rate, " + \
    # "change_in_5_mins ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " + \
    #     "%s, %s, %s, %s, %s, %s)"
    # effect_row2 = cursor.execute(sql, [("jack"), ("boom"), ("lucy")])
    # # 查询所有数据,返回数据为元组格式
    # result = cursor.fetchall()
    # conn.commit()
    # cursor.close()
    # conn.close()

    pass

@supports.func_execution_timer
@logger.catch
def execute():
    if not supports.today_market_open():
        logger.info("China finance market is not open today")
        return
    
    data_file_path = get_data_file_name_path()
    df = download_and_save_zh_stock(data_file_path)
        
    # data_file_path = supports.PATH_DATA / "2023-12-27/stock_zh_1717.pkl"

    # with open(data_file_path, "rb") as f:
    #     df = pickle.load(f)
    #     print(list(df))
    
    time_str = data_file_path.stem.split('_')[2]
    time_str = f"{time_str[0:2]}:{time_str[2:]}"

    date_str = data_file_path.parts[-2]

    generate_min_price_files(df, date_str, time_str)

if __name__ == '__main__':
    supports.init_app("mins_data_analysis")
    
    execute()
