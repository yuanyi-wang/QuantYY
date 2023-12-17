import os
import pickle

import akshare as ak
from loguru import logger

import common.supports as supports


@logger.catch()
def get_data_file_name():
    formatted_time = supports.get_now().strftime('%H%M')
    file_name = f"stock_zh_{formatted_time}.pkl"
    data_folder_name = supports.get_today_data_folder()
    if not os.path.exists(data_folder_name) :
        os.makedirs(data_folder_name)

    data_file = os.path.join(data_folder_name, file_name)
    return data_file


@logger.catch()
def download_and_save_zh_stock(data_file):
    stock_zh = ak.stock_zh_a_spot_em()
    with open(data_file, 'wb') as file:
        pickle.dump(stock_zh, file)
        logger.info(f'Object successfully saved to "{data_file}"')

if __name__ == '__main__':
    supports.init_app("2mins_data_analysis")
    
    logger.info("2 minutes data analysis start")
    
    if supports.today_market_open():
        data_file = get_data_file_name()
        download_and_save_zh_stock(data_file)
    else:
        logger.info("China finance market is not open today")
