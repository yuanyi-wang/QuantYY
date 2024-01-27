# -*-coding:utf-8 -*-

"""
1. 基于最后一个价格文件，更新每日价格文件
2. 计算最近5个交易日,10个交易日,20交易日,100交易日,52周平均价格
"""

from concurrent.futures import ThreadPoolExecutor

from common import supports


def update_daily_price():
    def _update_daily_price(data_path):
        pass

    with ThreadPoolExecutor(max_workers=supports.CPU_COUNT - 1) as thread_pool:
        pass


def calculate_avg_price():
    pass


def execute():
    if not supports.today_market_open():
        return

    update_daily_price()
    calculate_avg_price()


if __name__ == "__main__":
    supports.init_app("zh_stock_daily_after_close")
    execute()
