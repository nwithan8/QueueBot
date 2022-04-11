from modules.base_config import BaseConfig


class QueueBotConfig(BaseConfig):
    def __init__(self, config_file: str):
        super().__init__(app_name="QueueBot", config_file=config_file)
