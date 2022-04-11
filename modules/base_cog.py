from typing import List

import discord
from discord.ext.commands import Cog

from modules.cog_config import CogConfig
from modules.discord_utils import get_users, get_roles


class BaseCog(Cog):
    def __init__(self, bot: discord.Bot, config: CogConfig):
        self.bot = bot
        self.config = config

    @property
    def admin_role_names(self) -> List[str]:
        return self.config.admin_role_names

    def get_admin_roles(self, guild: discord.Guild) -> List[discord.Role]:
        return get_roles(guild=guild, role_names=self.admin_role_names)

    @property
    def admin_ids(self) -> List[int]:
        return self.config.admin_ids

    def get_admin_users(self, guild: discord.Guild) -> List[discord.Member]:
        return get_users(guild=guild, user_ids=self.admin_ids)
