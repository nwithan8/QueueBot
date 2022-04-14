from typing import Union, Optional

import discord
from discord import Option
from discord.ext.bridge import bridge_command, BridgeContext
from discord.ext.commands import Context
from discord.commands import SlashCommandGroup

from modules.base_cog import BaseCog, SlashCommand
from modules.discord_utils import send_error, is_admin, user_is_admin
from modules.utils import int_to_place
from queue_bot_database import QueueDatabase, UserQueueEntry
from queues.queue_bot_base import QueueBotBase


class QueueBotUsers(QueueBotBase):
    def __init__(self, bot):
        super().__init__(bot=bot)
        self.database = QueueDatabase(sqlite_file="queue.db", table_schemas=[UserQueueEntry])

        # need to make this group dynamically
        self.users_group = SlashCommandGroup(name="users", description="Commands related to queuing users.",
                                             parent=self.queue_group)
        self.register_slash_command_groups(groups=[
            self.users_group
        ])

        self.register_slash_commands(commands=[
            SlashCommand(name="add", func=self.queue_add, group=self.users_group),
            SlashCommand(name="remove", func=self.queue_remove, group=self.users_group),
            SlashCommand(name="place", func=self.queue_place, group=self.users_group),
            SlashCommand(name="next", func=self.queue_next, group=self.users_group),
            SlashCommand(name="export", func=self.queue_export, group=self.users_group),
        ])

    async def queue_add(self, ctx: BridgeContext):
        """
        Adds yourself to the queue.
        """
        user_id = ctx.author.id
        if self.database.get_user_from_queue(user_id=user_id):
            await ctx.send("You are already in the queue!")
            return
        if self.database.add_user_to_queue(user_id=user_id):
            await ctx.send("You have been added to the queue!")
            return
        await send_error(ctx=ctx)

    async def queue_remove(self, ctx: BridgeContext, user: Option(discord.Member, "user", required=False)):
        """
        Remove yourself from the queue.
        """
        if user:
            if not await user_is_admin(self, ctx=ctx):
                await send_error(ctx=ctx,
                                 error_message="You do not have permission to remove other users from the queue!")
                return
            user_id = user.id
            if not self.database.get_user_from_queue(user_id=user_id):
                await ctx.send("That user is not in the queue!")
                return
            self.database.delete_user_from_queue(user_id=user_id)  # always returns true
            await ctx.send(f"<@{user_id}> has been removed from the queue!")
        else:
            user_id = ctx.author.id
            if not self.database.get_user_from_queue(user_id=user_id):
                await ctx.send("You are not in the queue!")
                return
            self.database.delete_user_from_queue(user_id=user_id)  # always returns true
            await ctx.send(f"You has been removed from the queue!")

    async def queue_place(self, ctx: BridgeContext):
        """
        See where you are in the queue
        """
        user_id = ctx.author.id
        user_location = self.database.find_user_location_in_queue(user_id=user_id)
        if not user_location:
            await ctx.send("You are not in the queue!")
            return
        await ctx.send(f"You are currently {int_to_place(user_location)} in the queue!")

    @is_admin
    async def queue_next(self, ctx: BridgeContext):
        """
        See who is next in the queue
        """
        next_user = self.database.get_next_user_from_queue()
        if not next_user:
            await ctx.send("There is no one in the queue!")
            return
        await ctx.send(f"The next user in the queue is <@{next_user.user_id}>!")

    @is_admin
    async def queue_export(self, ctx: BridgeContext):
        """
        Export the queue to a CSV.
        """
        # await is_admin(cog=self, ctx=ctx)
        if not self.database.export_user_queue_to_csv("queue.csv"):
            await send_error(ctx=ctx)
            return
        await ctx.send(file=discord.File("queue.csv"))
