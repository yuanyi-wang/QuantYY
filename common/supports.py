# -*-coding:utf-8 -*-

from datetime import datetime
import json
import os
import time
import sys

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

def now():
    """
    取得当前时间
    """
    return datetime.now()

# 应用目录
project_folder = os.getcwd()
logger.debug(f"project_folder = {project_folder}")

# 获取 common_data
with open(os.path.join(project_folder, "data.json"), 'r') as f:
    data_json = json.load(f)
common_data = data_json

# 获取配置
with open(os.path.join(project_folder, "secrets.json"), 'r') as f:
    secrets_json = json.load(f)
configuration = secrets_json

cfg_path_data = configuration["path"]["data"]
cfg_path_logs = configuration["path"]["logs"]

# 是否打印 DEBUG 日志
DEBUG = False


def get_today_data_folder():
    formatted_date = now().strftime('%Y-%m-%d')
    return os.path.join(cfg_path_data, formatted_date)


def config_logger(logger_name, debug):
    """
    配置日志
    """
    # 每天一个日志
    logFile = os.path.join(cfg_path_logs, "{time:YYYY_MM_DD}", f"{logger_name}.log")
    
    # ERROR及以上 的日志单独保存
    error_logFile = os.path.join(cfg_path_logs, "error.log")
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
    formatted_date = now().strftime('%Y-%m-%d')
    return not(now().weekday() in [5, 6] or formatted_date in common_data["holidays"])
    

def func_execution_timer(func):
    """
    函数执行计时器
    """

    def inner(*arg,**kwarg):
        s_time = time.time()
        func_name = f"{func.__module__}.{func.__name__}"
        res = func(*arg,**kwarg)
        e_time = time.time()
        
        logger.info(f"Execute {func_name} function used {e_time - s_time}s")
        return res
    return inner