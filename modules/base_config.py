from modules.config_parser import ConfigParser


class BaseConfig(ConfigParser):
    def __init__(self, app_name: str, config_file: str):
        super().__init__(app_name=app_name, config_file=config_file)

    @property
    def log_level(self):
        return self.get(key='Logging', default='INFO')

    @property
    def bot_token(self):
        return self.get(key='BotToken', path=['Discord'], default=None)

    @property
    def server_id(self):
        return self.get(key='ServerID', path=['Discord'], default=None)

    @property
    def admin_ids(self):
        return self.get(key='AdminIDs', path=["Discord"], default=[])

    @property
    def admin_role_names(self):
        return self.get(key='AdminRoleNames', path=['Discord'], default=[])

    @property
    def allow_analytics(self):
        return self.get(key='Analytics', path=['Extras'], default=False)
