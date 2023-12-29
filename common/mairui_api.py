# -*-coding:utf-8 -*-

import requests
from urllib import parse

from loguru import logger

import common.supports as supports

try:
    license_list = supports.APP_CONFIG["api"]["mairui"]
except Exception as e:
    logger.error("Please config [\"api\"][\"mairui\"]")
    raise e
    
if len(license_list) == 0:
    logger.error("Did not find Mairui license")
    raise Exception("Did not find Mairui license")

@logger.catch
def _mairui_api_get(url):
    
    for license in license_list:
        get_url = parse.urljoin(url, license)
        logger.debug(get_url)
        response = requests.get(get_url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.info(f"Can't get {url}, continue to try next license - {response.status_code} \n {response.reason}")
    
    logger.error(f"Get {url} error - {response.status_code} \n {response.reason}")
    return None

def get_all_zh_stock_names():
    """
    全部股票代码:名称
    """
    return _mairui_api_get("http://api.mairui.club/hslt/list/")

def get_new_stock_calendar():
    """
    新股日历
    """
    return _mairui_api_get("http://api.mairui.club/hslt/new/")
    
def get_trend_of_main_funds(stock_list: list) -> list:
    """
    主力资金
    """
    result_list = list
    for stock_code in stock_list:
        result_list.append(_mairui_api_get(f"http://api.mairui.club/hsmy/zlzj/{stock_code}/"))

    return result_list


