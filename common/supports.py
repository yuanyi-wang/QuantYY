# -*-coding:utf-8 -*-
"""
Provide supporting functions
"""


import os
import time
import sys
from datetime import datetime
import json
import math


import multiprocessing
from pathlib import Path
from jsonpath import jsonpath

from loguru import logger


def init_app(logger_name, debug=False):
    """
    初始化程序
    """
    # 设置时区
    os.environ["TZ"] = "Asia/Shanghai"
    time.tzset()
    config_logger(logger_name, debug)
    logger.info(f"Start arguments: {sys.argv}")
    logger.info(f"Environment variables: {os.environ}")
    logger.info(f"Path: {sys.path}")
    logger.info(f"Platform: {sys.platform}")


def _now():
    """
    取得当前时间
    """
    return datetime.now()


def today() -> str:
    """
    today string
    """
    return _now().strftime("%Y-%m-%d")


def today1() -> str:
    """
    today string without "-"
    """
    return _now().strftime("%Y%m%d")


def now() -> str:
    """
    now string
    """
    return _now().strftime("%H:%M")


def now1() -> str:
    """ 
    now string without ":"
    """
    return _now().strftime("%H%M")


# 应用目录
_project_folder = Path(__file__).parent.parent.absolute()
logger.debug(f"project_folder = {_project_folder}")

PATH_APP_ROOT = Path(_project_folder)

# 获取 common_data
with open(PATH_APP_ROOT / "data.json", "r", encoding="utf-8") as f:
    data_json = json.load(f)
COMMON_DATA = data_json

# 获取配置
with open(PATH_APP_ROOT / "secrets.json", "r", encoding="utf-8") as f:
    secrets_json = json.load(f)
APP_CONFIG = secrets_json

# 获取 stock 配置数据
with open(PATH_APP_ROOT / "stock.json", "r", encoding="utf-8") as f:
    stock_json = json.load(f)
STOCK_DATA = stock_json

PATH_DATA = Path(APP_CONFIG["path"]["data"])
PATH_LOGS = Path(APP_CONFIG["path"]["logs"])

# 是否打印 DEBUG 日志
DEBUG = False


def is_dev() -> bool:
    """ 
    whether this is dev environment
    """
    return (PATH_APP_ROOT / "dev.flag").exists()


def get_today_data_path() -> Path:
    """
    
    """
    formatted_date = today()
    return PATH_DATA / formatted_date


def config_logger(logger_name, debug):
    """
    配置日志
    """
    # 每天一个日志
    log_file = PATH_LOGS / "{time:YYYY_MM_DD}" / f"{logger_name}.log"

    # ERROR及以上 的日志单独保存
    error_log_file = PATH_LOGS / "error.log"

    logger.add(error_log_file, level="ERROR")

    if debug:
        logger.add(
            log_file,
            level="TRACE",
            rotation="00:00",
            compression="zip",
            retention="30days",
        )
    else:
        # 默认只保存INFO级别之日
        logger.add(
            log_file,
            level="INFO",
            rotation="00:00",
            compression="zip",
            retention="30days",
        )


def today_market_open():
    """
    今天是否是交易日
    """
    if is_dev():
        logger.info("This is DEV environment, ignore market opening check")
        return True

    return not (_now().weekday() in [5, 6] or now() in COMMON_DATA["holidays"])


def func_execution_timer(func):
    """
    函数执行计时器
    """

    def inner(*arg, **kwarg):
        func_name = f"{func.__module__}.{func.__name__}"
        logger.info(f"Start to execute {func_name}")
        s_time = time.time()
        res = func(*arg, **kwarg)
        e_time = time.time()
        logger.info(f"Execute {func_name} function used {e_time - s_time}s")
        return res

    return inner


CPU_COUNT = multiprocessing.cpu_count()
logger.info(f"CPU: {CPU_COUNT}")


def get_app_config(key: str, default_value=None):
    """
    get configuration value using key
    """
    exp = "$." + key  # + "[0]"
    v = jsonpath(APP_CONFIG, exp)[0]

    if not v:
        return default_value
    return v


@logger.catch
def dump_json_to_file(json_data, folder_path, file_name):
    """
    dump json object to a file
    """
    if json_data is None:
        logger.info(f"{file_name} is None, do not save")
        return

    if not folder_path.exists():
        # create base folder
        os.makedirs(folder_path)

    file_path = folder_path / file_name
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"save {file_name} successfully")


def j(v):
    """
    convert NaN as None
    """
    if math.isnan(v):
        return None
    return v
