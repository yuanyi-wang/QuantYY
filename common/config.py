# -*-coding:utf-8 -*-

import json
import os
import supports


class quant_yy_config():
    def __init__():
        os.path.join(supports.get_project_root_folder, "config.json")
        with open(os.path.join(supports.get_project_root_folder, "config.json"), 'r') as f:
            json.load(f)
    
    data = None

    # def get_config():
    #     return data
    