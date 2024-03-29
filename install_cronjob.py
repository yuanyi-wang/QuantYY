# -*-coding:utf-8 -*-

"""
20 0,12 * * * /home/yuanyi/Workspaces/QuantYY/quant_yy_supports/pull_latest_code.sh > 
/home/yuanyi/Workspaces/QuantYY/quant_yy/logs/pull_latest_code.log

"""

import getpass

from crontab import CronTab
from loguru import logger

from common import supports

supports.init_app("crontab_job_setup")

user = supports.get_app_config("crontab.user") or getpass.getuser()
command_line = (supports.PATH_APP_ROOT / "run_job.sh").as_posix()

with CronTab(user=user) as cron:
    # remove all existing cron jobs
    cron.remove_all()

    # 开盘前数据加载 周一到周五 每天 9:15 执行

    zh_stock_daily_before_opening_job = cron.new(
        command=command_line + " zh_stock_daily_before_opening",
        comment="开盘前数据加载 周一到周五 每天 9:15 执行",
    )
    zh_stock_daily_before_opening_job.setall("28 9 * * 1-5")

    zh_stock_min_price_load_job_0 = cron.new(
        command=command_line + " zh_stock_min_price_load",
        comment="获取大陆股票价格信息, 交易日每2分钟执行一次",
    )
    zh_stock_min_price_load_job_0.setall("20-59/2 9 * * 1-5")

    zh_stock_min_price_load_job_1 = cron.new(
        command=command_line + " zh_stock_min_price_load",
        comment="获取大陆股票价格信息, 交易日每2分钟执行一次",
    )
    zh_stock_min_price_load_job_1.setall("*/2 10 * * 1-5")

    zh_stock_min_price_load_job_2 = cron.new(
        command=command_line + " zh_stock_min_price_load",
        comment="获取大陆股票价格信息, 交易日每2分钟执行一次",
    )
    zh_stock_min_price_load_job_2.setall("0-32/2 11 * * 1-5")

    zh_stock_min_price_load_job_3 = cron.new(
        command=command_line + " zh_stock_min_price_load",
        comment="获取大陆股票价格信息, 交易日每2分钟执行一次",
    )
    zh_stock_min_price_load_job_3.setall("*/2 13-14 * * 1-5")

    zh_stock_min_price_load_job_4 = cron.new(
        command=command_line + " zh_stock_min_price_load",
        comment="获取大陆股票价格信息, 交易日每2分钟执行一次",
    )
    zh_stock_min_price_load_job_4.setall("0-6/2 15 * * 1-5")

    zh_stock_daily_after_close_job = cron.new(
        command=command_line + " zh_stock_daily_after_close",
        comment="交易日数据整理 周一到周五 每天 18:00 执行",
    )
    zh_stock_daily_after_close_job.setall("0 18 * * 1-5")

logger.info("Setup cron jobs complete")
