import os
from functools import lru_cache

import yaml

default_config_file = "config.yaml"

def get_project_dir():
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

@lru_cache(maxsize=1)
def load_config():
    config_path = get_project_dir() + "data/." + default_config_file
    print(config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "找不到data/.config.yaml文件，请按教程确认该配置文件是否存在"
        )
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config
