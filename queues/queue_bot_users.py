import discord
from discord import Option
from discord.ext.bridge import bridge_command, BridgeContext
from discord.commands import SlashCommandGroup

from dbotbase.base_cog import BaseCog, SlashCommand
from dbotbase.discord_utils import send_error, is_admin, user_is_admin
from modules.utils import int_to_place
from queue_bot_database import QueueDatabase, UserQueueEntry
from queues.queue_bot_base import QueueBotBase


class QueueBotUsers(QueueBotBase):
    users_group = SlashCommandGroup(name="user-queue", description="Commands related to queuing users.")

    def __init__(self, bot):
        super().__init__(bot=bot)
        self.users_queue_database = QueueDatabase(sqlite_file="queue.db", table_schemas=[UserQueueEntry])

    @users_group.command(name="add")
    async def queue_add(self, ctx: BridgeContext):
        """
        Adds yourself to the queue.
        """
        user_id = ctx.author.id
        if self.users_queue_database.get_user_from_queue(user_id=user_id):
            await ctx.send("You are already in the queue!")
            return
        if self.users_queue_database.add_user_to_queue(user_id=user_id):
            await ctx.send("You have been added to the queue!")
            return
        await send_error(ctx=ctx)

    @users_group.command(name="remove")
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
            if not self.users_queue_database.get_user_from_queue(user_id=user_id):
                await ctx.send("That user is not in the queue!")
                return
            self.users_queue_database.delete_user_from_queue(user_id=user_id)  # always returns true
            await ctx.send(f"<@{user_id}> has been removed from the queue!")
        else:
            user_id = ctx.author.id
            if not self.users_queue_database.get_user_from_queue(user_id=user_id):
                await ctx.send("You are not in the queue!")
                return
            self.users_queue_database.delete_user_from_queue(user_id=user_id)  # always returns true
            await ctx.send(f"You has been removed from the queue!")

    @users_group.command(name="place")
    async def queue_place(self, ctx: BridgeContext):
        """
        See where you are in the queue
        """
        user_id = ctx.author.id
        user_location = self.users_queue_database.find_user_location_in_queue(user_id=user_id)
        if not user_location:
            await ctx.send("You are not in the queue!")
            return
        await ctx.send(f"You are currently {int_to_place(user_location)} in the queue!")

    @users_group.command(name="next")
    @is_admin
    async def queue_next(self, ctx: BridgeContext):
        """
        See who is next in the queue
        """
        next_user = self.users_queue_database.get_next_user_from_queue()
        if not next_user:
            await ctx.send("There is no one in the queue!")
            return
        await ctx.send(f"The next user in the queue is <@{next_user.user_id}>!")

    @users_group.command(name="export")
    @is_admin
    async def queue_export(self, ctx: BridgeContext):
        """
        Export the queue to a CSV.
        """
        if not self.users_queue_database.export_user_queue_to_csv("user_queue.csv"):
            await send_error(ctx=ctx)
            return
        await ctx.send(file=discord.File("user_queue.csv"))
