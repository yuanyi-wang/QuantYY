# -*-coding:utf-8 -*-

from datetime import datetime
import json
import os
import time

from loguru import logger

def init_app(logger_name, debug = False):
    os.environ['TZ'] = "Asia/Shanghai"
    time.tzset()
    config_logger(logger_name, debug)

def now():
    return datetime.now()

project_folder = os.getcwd()
logger.debug(f"project_folder = {project_folder}")


with open(os.path.join(project_folder, "data.json"), 'r') as f:
    data_json = json.load(f)

common_data = data_json

with open(os.path.join(project_folder, "secrets.json"), 'r') as f:
    secrets_json = json.load(f)

configuration = secrets_json

def get_data_folder():
    data_folder = configuration["path"]["data"]
    return data_folder

def get_today_data_folder():
    formatted_date = now().strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)


_logs_folder = configuration["path"]["logs"]

DEBUG = False

def config_logger(logger_name, debug):
    logFile = os.path.join(_logs_folder, "{time: YYYY_MM_DD}", f"{logger_name}.log")
    error_logFile = os.path.join(_logs_folder, "error.log")
    logger.add(error_logFile, level="ERROR")

    if debug:
        logger.add(logFile, level="TRACE", rotation='00:00', compression='zip', retention="30days")
    else:
        logger.add(logFile, rotation='00:00', compression='zip', retention="30days")

def today_market_open():
    formatted_date = now().strftime('%Y-%m-%d')
    return not(now().weekday() in [5, 6] or formatted_date in common_data["holidays"])
    