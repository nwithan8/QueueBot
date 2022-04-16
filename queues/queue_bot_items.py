from typing import Union, Optional

import discord
from discord import Option
from discord.ext.bridge import bridge_command, BridgeContext
from discord.ext.commands import Context
from discord.commands import SlashCommandGroup

from dbotbase.base_cog import BaseCog, SlashCommand
from dbotbase.discord_utils import send_error, is_admin, user_is_admin
from queue_bot_database import QueueDatabase, ItemQueueEntry
from queues.queue_bot_base import QueueBotBase


class QueueBotItems(QueueBotBase):
    items_group = SlashCommandGroup(name="item-queue", description="Commands related to queuing items.")

    def __init__(self, bot):
        super().__init__(bot=bot)
        self.items_queue_database = QueueDatabase(sqlite_file="queue.db", table_schemas=[ItemQueueEntry])

    @items_group.command(name="export")
    @is_admin
    async def queue_export(self, ctx: BridgeContext):
        """
        Export the queue to a CSV.
        """
        if not self.users_queue_database.export_item_queue_to_csv("item_queue.csv"):
            await send_error(ctx=ctx)
            return
        await ctx.send(file=discord.File("item_queue.csv"))
