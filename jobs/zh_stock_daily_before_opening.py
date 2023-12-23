# -*-coding:utf-8 -*-

import os
import json

from loguru import logger

import common.supports as supports
import common.mairui_api as mairui

@logger.catch
def _save_json(json_data, file_name):

    if not json_data:
        logger.info(f"{file_name} is None, do not save")
        return

    data_folder = supports.configuration["path"]["data"]
    base_folder = os.path.join(data_folder, "zh_stocks")

    if not os.path.exists(base_folder):
        #create base folder
        os.mkdir(base_folder)

    file_path = os.path.join(base_folder, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        logger.debug(f"save {file_name} successfully")


@logger.catch
def execute():
    # 更新股票列表
    _save_json(mairui.get_all_zh_stock_names(), "all_zh_stock_names.json")
    # 更新新股日历
    _save_json(mairui.get_new_stock_calendar(), "new_stock_calendar.json")


if __name__ == '__main__':
    supports.init_app("daily_before_opening")

    logger.info("Start zh_stock_daily_before_opening job")

    execute()
