from datetime import date, datetime
import os
import pickle
import pytz

import akshare as ak
from loguru import logger

import common.supports as supports

def get_data_file_name():
    asia_shanghai = pytz.timezone('Asia/Shanghai')
    now = datetime.now(asia_shanghai)

    formatted_time = now.strftime('%H%M')
    file_name = f"stock_zh_{formatted_time}.pkl"
    data_folder_name = supports.get_today_data_folder()
    if not os.path.exists(data_folder_name) :
        os.makedirs(data_folder_name)

    data_file = os.path.join(data_folder_name, file_name)
    return data_file

def download_and_save_zh_stock(data_file):
    stock_zh = ak.stock_zh_a_spot_em()
    with open(data_file, 'wb') as file:
        pickle.dump(stock_zh, file)
        print(f'Object successfully saved to "{data_file}"')

if __name__ == '__main__':
    logger.info("2 minutes data analysis start")
    if supports.today_market_open():
        data_file = get_data_file_name()
        download_and_save_zh_stock(data_file)
    else:
        logger.info("China finance market is closed today")