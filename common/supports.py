# -*-coding:utf-8 -*-

from datetime import datetime
import json
import os
import time
import sys
import multiprocessing
from pathlib import Path

from loguru import logger

def init_app(logger_name, debug = False):
    """
    初始化程序
    """
    # 设置时区
    os.environ['TZ'] = "Asia/Shanghai"
    time.tzset()
    config_logger(logger_name, debug)
    logger.info(f"Start arguments: {sys.argv}")
    logger.info(f"Environment variables: {os.environ}")
    logger.info(f"Platform: {sys.platform}")

def _now():
    """
    取得当前时间
    """
    return datetime.now()

def todate() -> str:
    return _now().strftime('%Y-%m-%d')

def now() -> str:
    return _now().strftime('%H:%M')

# 应用目录
_project_folder = os.getcwd()
logger.debug(f"project_folder = {_project_folder}")

PATH_APP_ROOT = Path(_project_folder)

# 获取 common_data
with open(PATH_APP_ROOT / "data.json", 'r') as f:
    data_json = json.load(f)
COMMON_DATA = data_json

# 获取配置
with open(PATH_APP_ROOT / "secrets.json", 'r') as f:
    secrets_json = json.load(f)
APP_CONFIG = secrets_json

PATH_DATA = Path(APP_CONFIG["path"]["data"])
PATH_LOGS = Path(APP_CONFIG["path"]["logs"])

# 是否打印 DEBUG 日志
DEBUG = False


def get_today_data_path() -> Path:
    formatted_date = todate()
    return PATH_DATA / formatted_date


def config_logger(logger_name, debug):
    """
    配置日志
    """
    # 每天一个日志
    logFile = PATH_LOGS / "{time:YYYY_MM_DD}" / f"{logger_name}.log"
    
    # ERROR及以上 的日志单独保存
    error_logFile = PATH_LOGS / "error.log"
    logger.add(error_logFile, level="ERROR")

    if debug:
        logger.add(logFile, level="TRACE", rotation='00:00', compression='zip', retention="30days")
    else:
        # 默认只保存INFO级别之日
        logger.add(logFile, level="INFO", rotation='00:00', compression='zip', retention="30days")

def today_market_open():
    """
    今天是否是交易日
    """
    return not(_now().weekday() in [5, 6] or now() in COMMON_DATA["holidays"])
    

def func_execution_timer(func):
    """
    函数执行计时器
    """

    def inner(*arg,**kwarg):
        func_name = f"{func.__module__}.{func.__name__}"
        logger.info(f"Start to execute {func_name}")
        s_time = time.time()
        res = func(*arg,**kwarg)
        e_time = time.time()
        logger.info(f"Execute {func_name} function used {e_time - s_time}s")
        return res
    return inner

CPU_COUNT = multiprocessing.cpu_count()
logger.info(f"CPU: {CPU_COUNT}")