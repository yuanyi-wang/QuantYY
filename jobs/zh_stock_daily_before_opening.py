# -*-coding:utf-8 -*-

from loguru import logger
import QuantLib as ql

from common import supports
from common import zh_stock as stock
from common import constants as cs

CNY = ql.CNYCurrency()


@logger.catch
@supports.func_execution_timer
def execute():
    # 更新股票列表
    # _save_json(mairui.get_all_zh_stock_names(), "all_zh_stock_names.json")
    # 更新新股日历
    # json_data = ak.stock_new_ipo_cninfo().to_json(orient='records',
    # force_ascii = False, indent=4)[1:-1].replace('},{', '} {')
    # supports.dump_json_to_file(json_data, supports.PATH_DATA / "zh_stocks",
    # "new_stock_calendar.json")

    _get_holding_list_detail()


def _get_holding_list_detail():
    holdings = supports.STOCK_DATA["holdings"]
    holding_detail_list = []
    for holding in holdings:
        stock_today_data = stock.get_today_data(holding["stock_symbol"])
        summary = stock_today_data["summary"]
        holding_detail_list.append(
            {
                "stock_symbol": holding[cs.STOCK_SYMBOL],
                "stock_name": summary[cs.STOCK_NAME],
                "latest_price": summary[cs.LATEST_PRICE],
                "turnover_rate": summary[cs.TURNOVER_RATE],
                "holding": holding["holding"],
                "cost": holding["cost"],
                "total_cost": (
                    ql.Money(holding["cost"], CNY) * holding["holding"]
                ).value(),
                "total_value": summary["latest_price"] * holding["holding"],
                "growth": (
                    ql.Money((summary["latest_price"] - holding["cost"]), CNY)
                    * holding["holding"]
                ).value(),
            }
        )

    print(holding_detail_list)
    return holding_detail_list


if __name__ == "__main__":
    supports.init_app("daily_before_opening")

    logger.info("Start zh_stock_daily_before_opening job")

    execute()
