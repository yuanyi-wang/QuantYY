# -*-coding:utf-8 -*-

import requests

from loguru import logger

from supports import configuration as config

def _mairui_api_get(url):
    license_list = config["api"]["mairui"]

    for license in license_list:
        response = requests.get(url + license)
        if response.status_code == 200:
            return response.json()
        else:
            logger.info(f"Can't get {url} - {response.status_code} \n {response.reason}")
    
    logger.error(f"Get {url} error - {response.status_code} \n {response.reason}")
    return None

def get_all_zh_stock_names():
    return _mairui_api_get("http://api.mairui.club/hslt/list/")

def get_new_stock_calendar():
    return _mairui_api_get("http://api.mairui.club/hslt/new/")
    
def get_trend_of_main_funds(stock_list: list) -> list:
    result_list = list
    for stock_code in stock_list:
        result_list.append(_mairui_api_get(f"http://api.mairui.club/hsmy/zlzj/{stock_code}/"))

    return result_list


