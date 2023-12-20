# -*-coding:utf-8 -*-

import argparse

from loguru import logger

import jobs.zh_stock_min_price_load_job as zh_stock_min_price_load_job
import common.supports as supports


def execute_zh_stock_min_price_load_job():
    supports.init_app("mins_data_analysis")
    zh_stock_min_price_load_job.execute()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog='quant_yy_jobs_cli')
    
    parser.add_argument('--job_name', default="zh_stock_min_price_load_job")
    parser.add_argument('-d', '--debug')

    args = parser.parse_args()

    match args.job_name :
        case "zh_stock_min_price_load_job":
            execute_zh_stock_min_price_load_job()
        case _:
            logger.error(f"{args.job_name} did not found, please double check")