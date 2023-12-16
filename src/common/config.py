import json, os
import supports


class quant_yy_config():
    def __init__():
        os.path.join(supports.get_project_root_folder, "config.json")
        with open(os.path.join(supports.get_project_root_folder, "config.json"), 'r') as f:
            data = json.load(f)
    
    data = None

    # def get_config():
    #     return data
    