# -*-coding:utf-8 -*-

import argparse

from loguru import logger

from common import supports
from jobs import zh_stock_min_price_load
from jobs import zh_stock_daily_before_opening


jobs = {
    "zh_stock_min_price_load": zh_stock_min_price_load,
    "zh_stock_daily_before_opening": zh_stock_daily_before_opening
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='quant_yy_jobs_cli')
    
    parser.add_argument('--job_name', default="zh_stock_min_price_load")
    parser.add_argument('-d', '--debug', help="whether print debug log",
                    action="store_true")

    args = parser.parse_args()

    supports.init_app(args.job_name, args.debug)

    if args.job_name in jobs.keys():
        try:
            logger.info(f"********* {args.job_name} start *********")
            jobs[args.job_name].execute()
            logger.info(f"********* {args.job_name} complete *********")
        except Exception as e:
            logger.error(f"{args.job_name} get exception", e)
    else:
        logger.error(f"Can't find {args.job_name}, please check")