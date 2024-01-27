# -*-coding:utf-8 -*-

from loguru import logger

from common import supports
from zh_stocks import data as zh_stocks_data
from notifications import zh_stock_price_big_change_warn as warns


@supports.func_execution_timer
@logger.catch
def execute():
    if not supports.today_market_open():
        logger.info("China finance market is not open today")
        return

    zh_stocks_data.save_current_zh_stock_price_data(
        warns.zh_stock_price_big_change_warn
    )


if __name__ == "__main__":
    supports.init_app("mins_data_analysis")
    execute()
