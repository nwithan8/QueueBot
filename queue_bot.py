import discord
from discord.ext.bridge import bridge_command, BridgeContext

from queue_bot_configuration import QueueBotConfig
from modules.base_cog import BaseCog
from modules.discord_utils import send_error, is_admin
from modules.utils import int_to_place
from queue_bot_database import QueueDatabase, UserQueueEntry


class QueueBot(BaseCog, name="QueueBot"):
    def __init__(self, bot):
        super().__init__(bot=bot, config=QueueBotConfig(config_files=["queue_bot_config.yaml"]))
        self.database = QueueDatabase(sqlite_file="queue.db", table_schemas=[UserQueueEntry])

    @bridge_command(name="queue-ping", aliases=["qping"])
    @is_admin
    async def queue_ping(self, ctx: BridgeContext):
        """
        Test command to check if the bot is working.
        """
        # await is_admin(cog=self, ctx=ctx)
        await ctx.respond("Pong!")

    @bridge_command(name="queue-add", aliases=["qaad"])
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

    @bridge_command(name="queue-remove", aliases=["qremove"])
    async def queue_remove(self, ctx: BridgeContext):
        """
        Remove yourself from the queue.
        """
        user_id = ctx.author.id
        if not self.database.delete_user_from_queue(user_id=user_id):
            await ctx.send("You are not in the queue!")
            return
        await ctx.send("You have been removed from the queue!")

    @bridge_command(name="queue-place", aliases=["qplace"])
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

    @bridge_command(name="queue-next", aliases=["qnext"])
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

    @bridge_command(name="queue-export", aliases=["qexport"])
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


def setup(bot):
    bot.add_cog(QueueBot(bot))
