# -*-coding:utf-8 -*-

from loguru import logger

import common.supports as supports

@logger.catch
def execute():
    pass

if __name__ == '__main__':
    supports.init_app("daily_before_opening")

    logger.info("Start zh_stock_daily_before_opening job")

    execute()
