import discord
from discord import Option
from discord.ext.bridge import bridge_command, BridgeContext
from discord.ext.commands import Context
from discord.commands import SlashCommandGroup

from modules.base_cog import BaseCog
from queue_bot_configuration import QueueBotConfig
from queue_bot_database import QueueDatabase, UserQueueEntry


class QueueBotBase(BaseCog):
    # slash command groups
    queue_group = SlashCommandGroup(name="queue", description="Commands related to general queuing.")

    def __init__(self, bot):
        super().__init__(bot=bot, config=QueueBotConfig(config_files=["queue_bot_config.yaml"]))

    @queue_group.command(name="ping")
    async def queue_ping(self, ctx: Context):
        """
        Test command to check if the bot is working.
        """
        await ctx.send("Pong!")
