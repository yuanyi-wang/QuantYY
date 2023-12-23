# -*-coding:utf-8 -*-

import os
import pickle

import akshare as ak
from loguru import logger

import common.supports as supports

@logger.catch()
def get_data_file_name():
    formatted_time = supports.now().strftime('%H%M')
    file_name = f"stock_zh_{formatted_time}.pkl"
    data_folder_name = supports.get_today_data_folder()
    if not os.path.exists(data_folder_name) :
        os.makedirs(data_folder_name)

    data_file = os.path.join(data_folder_name, file_name)
    return data_file


@logger.catch()
def download_and_save_zh_stock(data_file):
    df_stock_zh = ak.stock_zh_a_spot_em()
    with open(data_file, 'wb') as file:
        pickle.dump(df_stock_zh, file)
        logger.info(f'Object successfully saved to "{data_file}"')

    return df_stock_zh

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
def execute():
    if supports.today_market_open():
        data_file = get_data_file_name()
        download_and_save_zh_stock(data_file)
    else:
        logger.info("China finance market is not open today")

if __name__ == '__main__':
    supports.init_app("mins_data_analysis")

    execute()
