# -*-coding:utf-8 -*-
"""
stock price big change notifications
"""
import json

from common import send_wechat as wechat
from common import supports


def whether_sent_today(stock_symbol) -> bool:
    """
    whether it's sent today
    """
    path_runtime = supports.PATH_DATA / "runtime"
    if not path_runtime.exists():
        path_runtime.mkdir()

    path_cfg_file = path_runtime / f"{supports.today()}.json"

    if path_cfg_file.exists():
        with open(path_cfg_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            sent_notifications = json_data.get("sent_notifications", [])
            return stock_symbol in sent_notifications
    else:
        with open(path_cfg_file, "w", encoding="utf-8") as f:
            json_data = {"sent_notifications": []}
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return False


def update_sent_today(stock_symbol):
    """
    更新今天是否发送过一次
    """
    path_cfg_file = supports.PATH_DATA / "runtime" / f"{supports.today()}.json"

    with open(path_cfg_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        sent_notifications_set = set(json_data.get("sent_notifications", []))
        sent_notifications_set.add(stock_symbol)
        json_data["sent_notifications"] = list(sent_notifications_set)
    with open(path_cfg_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def zh_stock_price_big_change_warn(stock_price):
    """
    价格有重大变动报警
    """
    stock_symbol = stock_price["代码"]
    sotck_name = stock_price["名称"]
    change_rate_in_5_mins = stock_price["5分钟涨跌"]
    change_rate_today = stock_price["涨跌幅"]

    if stock_symbol in supports.STOCK_DATA["interesting"]:
        if abs(change_rate_in_5_mins) > 3 or abs(change_rate_today) > 5:
            if not whether_sent_today(stock_symbol):
                wechat.send_message(
                    f"[{sotck_name}] 5min{change_rate_in_5_mins}, 今天{change_rate_today}",
                    "<table>"
                    + f"<tr><td>代码:</td>        <td style='text-align: right;'>{stock_price['代码']} </td></tr>"
                    + f"<tr><td>名称:</td>        <td style='text-align: right;'>{stock_price['名称']} </td></tr>"
                    + f"<tr><td>昨收:</td>        <td style='text-align: right;'>{stock_price['昨收']} </td></tr>"
                    + f"<tr><td>今开:</td>        <td style='text-align: right;'>{stock_price['今开']} </td></tr>"
                    + f"<tr><td>最高:</td>        <td style='text-align: right;'>{stock_price['最高']} </td></tr>"
                    + f"<tr><td>最低:</td>        <td style='text-align: right;'>{stock_price['最低']} </td></tr>"
                    + f"<tr><td>最新价:</td>      <td style='text-align: right;'>{stock_price['最新价']} </td></tr>"
                    + f"<tr><td>成交量:</td>      <td style='text-align: right;'>{stock_price['成交量']} </td></tr>"
                    + f"<tr><td>成交额:</td>      <td style='text-align: right;'>{stock_price['成交额']} </td></tr>"
                    + f"<tr><td>换手率:</td>      <td style='text-align: right;'>{stock_price['换手率']}% </td></tr>"
                    + f"<tr><td>5分钟涨跌:</td>   <td style='text-align: right;'>{stock_price['5分钟涨跌']}% </td></tr>"
                    + f"<tr><td>今日涨跌幅:</td>  <td style='text-align: right;'>{stock_price['涨跌幅']}%</td></tr>"
                    + "</table>",
                    url=f"https://quote.eastmoney.com/concept/sh{stock_symbol}.html",
                )
            update_sent_today(stock_symbol)
