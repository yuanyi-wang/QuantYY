# -*-coding:utf-8 -*-

from datetime import datetime
import json
import os
import time

from loguru import logger

def init_app(logger_name):
    os.environ['TZ'] = "Asia/Shanghai"
    time.tzset()
    config_logger(logger_name)

def now():
    return datetime.now()

def get_project_root_folder():
    project_folder = os.getcwd()
    return project_folder

with open(os.path.join(get_project_root_folder(), "data.json"), 'r') as f:
    data_json = json.load(f)

common_data = data_json

with open(os.path.join(get_project_root_folder(), "secrets.json"), 'r') as f:
    secrets_json = json.load(f)

configuration = secrets_json

def get_data_folder():
    data_folder = configuration["configuration"]["path"]["data"]
    return data_folder

def get_today_data_folder():
    formatted_date = now().strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)

def _get_logs_folder():
    logs_folder = configuration["configuration"]["path"]["logs"]
    return logs_folder

def config_logger(logger_name):
    logFile = os.path.join(_get_logs_folder(), logger_name + ".log")
    logger.add(logFile, rotation='00:00', compression='zip', retention="30days")

def today_market_open():
    formatted_date = now().strftime('%Y-%m-%d')
    return not(now().weekday() in [5, 6] or formatted_date in common_data["holidays"])
    