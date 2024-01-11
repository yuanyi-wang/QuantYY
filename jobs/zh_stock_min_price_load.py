# -*-coding:utf-8 -*-

import os
import pickle
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import json

import akshare as ak
from loguru import logger

import common.supports as supports
import common.send_wechat as wechat
import common.constants as cs

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

            logger.debug(f"Create thread task for {row['代码']}")
            task = threadPool.submit(_generate_min_price_file, row, date_str, time_str)
            tasklist.append(task)

    wait(tasklist, return_when=ALL_COMPLETED)
    tasklist.clear()

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
    if stock_symbol in supports.STOCK_DATA["intresting"]:
        if abs(row['5分钟涨跌']) > 3 or abs(row['涨跌幅']) > 5:
            if not _whether_sent_today(stock_symbol):
                wechat.send_message(f"[{sotck_name}] 价格有重大变动", \
                    "<table>" + \
                    f"<tr><td>代码:</td>        <td style='text-align: right;'>{row['代码']} </td></tr>" + \
                    f"<tr><td>名称:</td>        <td style='text-align: right;'>{row['名称']} </td></tr>" + \
                    f"<tr><td>今开:</td>        <td style='text-align: right;'>{row['今开']} </td></tr>" + \
                    f"<tr><td>最高:</td>        <td style='text-align: right;'>{row['最高']} </td></tr>" + \
                    f"<tr><td>最低:</td>        <td style='text-align: right;'>{row['最低']} </td></tr>" + \
                    f"<tr><td>最新价:</td>      <td style='text-align: right;'>{row['最新价']} </td></tr>" + \
                    f"<tr><td>成交量:</td>      <td style='text-align: right;'>{row['成交量']} </td></tr>" + \
                    f"<tr><td>成交额:</td>      <td style='text-align: right;'>{row['成交额']} </td></tr>" + \
                    f"<tr><td>换手率:</td>      <td style='text-align: right;'>{row['换手率']}% </td></tr>" + \
                    f"<tr><td>5分钟涨跌:</td>   <td style='text-align: right;'>{row['5分钟涨跌']}% </td></tr>" + \
                    f"<tr><td>今日涨跌幅:</td>  <td style='text-align: right;'>{row['涨跌幅']}%</td></tr>" + \
                    "</table>",
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
    

    stock_symbol = row["代码"]
    item = {
        cs.TIME: str_time,
        cs.LATEST_PRICE: row['最新价']
    }
    summary = {
        cs.DATE:                str_date,
        cs.OPEN_PRICE:          row['今开'],
        cs.HIGHEST_PRICE:       row['最高'],
        cs.LOWEST_PRICE:        row['最低'],
        cs.TRANSACTION_VOLUME:  row['成交量'],
        cs.TRANSACTION_VALUE:   row['成交额'],
        cs.TURNOVER_RATE:       row['换手率']
    }

    file_data_folder_path = supports.PATH_DATA / "zh_stocks" / stock_symbol[0] / stock_symbol

    if not file_data_folder_path.exists():
        os.makedirs(file_data_folder_path)
    
    file_full_path = file_data_folder_path / f"{str_date}.json"
    
    def __generate_file_header(stock):
        stock["summary"] = summary

    def __generate_min_price_item(stock):
        if len(stock["prices"]) > 0 and stock["prices"][-1][cs.TIME] == str_time:
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
