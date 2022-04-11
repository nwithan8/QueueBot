from typing import List

from modules.bot_config import BotConfig


class CogConfig(BotConfig):
    def __init__(self, app_name: str, config_files: List[str] = None):
        super().__init__(app_name=app_name, config_files=config_files)

    @property
    def admin_ids(self):
        return self.get(key='AdminIDs', path=["Discord"], default=[])

    @property
    def admin_role_names(self):
        return self.get(key='AdminRoleNames', path=['Discord'], default=[])
