from datetime import date
import json
import os

def get_project_root_folder():
    project_folder = os.getcwd()
    return project_folder

def get_data_folder():
    data_folder = os.path.join(get_project_root_folder(), "data")
    return data_folder

def get_today_data_folder():
    formatted_date = date.today().strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)

def today_market_open():
    config_file = os.path.join(get_project_root_folder(), "config.json")
    with open(config_file, 'r') as f:
        data = json.load(f)
    formatted_date = date.today().strftime('%Y-%m-%d')
    return not(date.today().weekday() in [5, 6] or formatted_date in data["holidays"])
    