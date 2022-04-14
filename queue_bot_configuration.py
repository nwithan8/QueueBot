from typing import List

from modules.cog_config import CogConfig


class QueueBotConfig(CogConfig):
    def __init__(self, config_files: List[str]):
        super().__init__(app_name="QueueBot", config_files=config_files)

    @property
    def queue_types(self):
        return self.get(key='QueueTypes', default=[])
