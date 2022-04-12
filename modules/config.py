from typing import List

import yaml
import mergedeep
from mergedeep import Strategy


class Config:
    def __init__(self, app_name: str, config_files: List[str]):
        self.app_name = app_name
        self.config = {}
        for config_file in config_files:
            with open(config_file, "r") as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                mergedeep.merge(self.config, data, strategy=Strategy.REPLACE)

    def get(self, key: str, path: List[str] = None, default=None):
        try:
            if path is None:
                path = []
            value = self.config
            for p in path:
                value = value[p]
            return value.get(key, default)
        except KeyError:
            return default
