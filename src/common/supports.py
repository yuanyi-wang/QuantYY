from datetime import date
import os

def get_data_folder():
    
    # formatted_time = today.strftime('%H%M')

    # file_name = f"stock_zh_{formatted_time}.pkl"

    project_folder = os.getcwd()
    data_folder = os.path.join(project_folder, "data")
    return data_folder

def get_today_data_folder():
    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    return os.path.join(get_data_folder(), formatted_date)