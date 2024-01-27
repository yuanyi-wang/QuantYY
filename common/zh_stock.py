# -*-coding:utf-8 -*-

import json

from common import supports
from common import constants as cs

ZH_STOCKS_DATA_PATH = supports.PATH_DATA / "zh_stocks"


def get_today_latest_price(stock_symbol_list) -> dict:
    latest_price_dict = {}

    for stock_symbol in stock_symbol_list:
        stock_today_data = get_today_data(stock_symbol)
        if stock_today_data is not None:
            latest_price_dict[stock_symbol] = stock_today_data["summary"][
                cs.LATEST_PRICE
            ]

    return latest_price_dict


def get_today_data(stock_symbol):
    stock_today_data_file = (
        ZH_STOCKS_DATA_PATH
        / stock_symbol[0]
        / stock_symbol
        / f"{supports.today()}.json"
    )
    if not stock_today_data_file.exists():
        return None

    with open(
        ZH_STOCKS_DATA_PATH
        / stock_symbol[0]
        / stock_symbol
        / f"{supports.today()}.json",
        "r", encoding="utf-8"
    ) as f:
        data_json = json.load(f)

    return data_json


if __name__ == "__main__":
    print(get_today_latest_price(["000001", "300688"]))
