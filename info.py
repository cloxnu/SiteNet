import os
import yaml


def read_info():
    current_path = os.path.dirname(__file__)
    with open(current_path + '/info.yml') as f:
        return yaml.safe_load(f)
