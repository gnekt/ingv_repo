import os
import shutil
import json

config_path = "C:\\Users\\dima9\\OneDrive - studenti.unisa.it\\Desktop\\TIROCINIO\\webApp\\cfg\\configuration.json"
config = json.load((open(config_path, "r")))


def copy_folders(src, dst):
    for dir in os.listdir(src):
        if os.path.isdir(src + dir):
            shutil.copytree(src + dir, dst + dir)


def custom_bar(current, total, width=80):
    print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))


def retrieve_config_value(search_keys):
    temp_config = config
    for key in search_keys:
        try:
            temp_config = temp_config[key]
        except Exception:
            raise Exception("key not found")
    return temp_config
