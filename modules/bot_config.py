import logging
from typing import List

from modules.config import Config


class BotConfig(Config):
    def __init__(self, app_name: str, config_files: List[str] = None):
        if config_files is None:
            config_files = []
        config_files.append('bot_config.yaml')
        super().__init__(app_name=app_name, config_files=config_files)

    @property
    def log_level(self):
        level = self.get(key='Logging', default='INFO')
        return logging.getLevelName(level)

    @property
    def bot_token(self):
        return self.get(key='BotToken', path=['Discord'], default=None)

    @property
    def bot_prefix(self):
        return self.get(key='BotPrefix', path=['Discord'], default=None)

    @property
    def server_id(self):
        return self.get(key='ServerID', path=['Discord'], default=None)

    @property
    def allow_analytics(self):
        return self.get(key='Analytics', path=['Extras'], default=False)
