# -*-coding:utf-8 -*-

"""

"""

from common import supports

def get_holding_list():
    path_holding = supports.PATH_APP_ROOT / "holdings.txt"
    holding_list = []
    with open(path_holding, "r", encoding="gb18030") as f:
        lines = f.readlines()

        for line in lines[1:]:
            items = line.split("\t")
            holding = {}
            holding["股票代码"] = items[0]
            holding["可用股份"] = items[4]
            holding["成本价"] = items[6]
            holding_list.append(holding)
    print(holding_list)
    return holding_list

if __name__ == "__main__":
    get_holding_list()
