# -*-coding:utf-8 -*-

import os
import json

from loguru import logger

from common import supports


@logger.catch
def parse_and_transfer(file_path, market_code):
    with open(file_path, "r", encoding="gb2312") as f:
        stock_code = f.readline().split(" ")[0]
        f.readline()  # 忽略第二行
        line = f.readline()  # 读取第三行

        stock_daily_price = []

        while True:
            es = line.split("\t")
            line_x = f.readline()
            if line_x == "":
                break

            day_price = {
                "date": es[0].replace("/", "-"),
                "open_price": float(es[1]),
                "highest_price": float(es[2]),
                "lowest_price": float(es[3]),
                "close_price": float(es[4]),
                "transaction_volume": float(es[5]),
                "transaction_value": float(es[6].strip()),
            }
            stock_daily_price.append(day_price)

            line = line_x

    logger.info(f"Total {len(stock_daily_price)} for {stock_code} daily price")

    target_base_folder = os.path.join(
        supports.PATH_DATA, "zh_stocks", market_code, stock_code
    )

    if not os.path.exists(target_base_folder):
        os.makedirs(target_base_folder)

    target_file_path = os.path.join(target_base_folder, "daily_price.json")

    with open(target_file_path, "w", encoding="utf-8") as f:
        json.dump(stock_daily_price, f, ensure_ascii=False, indent=4)

    logger.info(f"Save {stock_code} daily price into {target_file_path}")


@logger.catch
@supports.func_execution_timer
def execute():
    export_folder = os.path.join(supports.PATH_DATA, "export")
    export_files = os.listdir(export_folder)

    logger.debug(f"Get {len(export_files)} files")

    for file_name in export_files:
        logger.info(f"Handle {file_name}")
        file_path = os.path.join(export_folder, file_name)
        if os.path.isfile(file_path):
            market_code = file_name.split("#")[0]
            parse_and_transfer(file_path, market_code)
        else:
            logger.info(f"{file_name} is not file, ignore")


if __name__ == "__main__":
    supports.init_app("transfer_txd_export_file_as_json")
    logger.info("Start transfer_txd_export_file_as_json job")
    execute()
