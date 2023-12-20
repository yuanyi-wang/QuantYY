# -*-coding:utf-8 -*-

from datetime import datetime
import json
import os
import time

from loguru import logger

def init_app(script_name):
    os.environ['TZ'] = "Asia/Shanghai"
    time.tzset()
    config_logger(script_name)

def now():
    return datetime.now()

def get_project_root_folder():
    project_folder = os.getcwd()
    return project_folder

def get_data_folder():
    data_folder = os.path.join(get_project_root_folder(), "data")
    return data_folder

def get_today_data_folder():
    formatted_date = now().strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)

def get_logs_folder():
    logs_folder = os.path.join(get_project_root_folder(), "logs")
    return logs_folder



def config_logger(script_name):
    logFile = os.path.join(get_logs_folder(), script_name + "_{time}.log")
    logger.add(logFile, rotation='12:00', compression='zip', retention="72h")
     
os.path.join(get_project_root_folder(), "config.json")
with open(os.path.join(get_project_root_folder(), "config.json"), 'r') as f:
    holidays_json = json.load(f)

holidays = holidays_json["holidays"]

def today_market_open():

    formatted_date = now().strftime('%Y-%m-%d')
    return not(now().weekday() in [5, 6] or formatted_date in holidays)
    