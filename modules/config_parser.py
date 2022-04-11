from typing import List

import confuse


class ConfigParser:
    def __init__(self, app_name: str, config_file: str):
        self.config = confuse.Configuration(app_name)
        self.config.set_file(filename=config_file)

    def get(self, key: str, path: List[str] = None, default=None):
        try:
            if path is None:
                path = []
            value = self.config
            for p in path:
                value = value[p].get()
            return value.get(key)
        except confuse.NotFoundError:
            return default
