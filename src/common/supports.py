from datetime import datetime
import json
import os
import time

from loguru import logger
import pytz

def init_app(script_name):
    os.environ['TZ'] = "Asia/Shanghai"
    time.tzset()
    config_logger(script_name)

def get_project_root_folder():
    project_folder = os.getcwd()
    return project_folder

def get_data_folder():
    data_folder = os.path.join(get_project_root_folder(), "data")
    return data_folder

def get_today_data_folder():
    formatted_date = get_now().strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)

def get_logs_folder():
    logs_folder = os.path.join(get_project_root_folder(), "logs")
    return logs_folder



def config_logger(script_name):
    logFile = os.path.join(get_logs_folder(), script_name + "_{time}.log")
    logger.add(logFile, rotation='12:00', compression='zip', retention="72h")
     


def today_market_open():
    config_file = os.path.join(get_project_root_folder(), "holidays.json")
    with open(config_file, 'r') as f:
        data = json.load(f)
    formatted_date = get_now().strftime('%Y-%m-%d')
    return not(get_now().weekday() in [5, 6] or formatted_date in data["holidays"])
    


def get_now():
    asia_shanghai = pytz.timezone('Asia/Shanghai')
    return datetime.now(asia_shanghai)