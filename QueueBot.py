import discord
from discord.ext.bridge import bridge_command, BridgeContext
from discord.ext.commands import Cog

from modules.queue_database import QueueDatabase, UserQueueEntry


async def send_error(ctx: BridgeContext, error_message: str = "Something went wrong!"):
    await ctx.respond(error_message)


class QueueBot(Cog, name="QueueBot"):
    def __init__(self, bot):
        self.bot = bot
        self.database = QueueDatabase(sqlite_file="queue.db", table_schemas=[UserQueueEntry])

    @bridge_command(name="queue-ping", aliases=["qp"])
    async def queue_ping(self, ctx: BridgeContext):
        """
        Test command to check if the bot is working.
        """
        await ctx.respond("Pong!")

    @bridge_command(name="queue-add", aliases=["qa"])
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

    @bridge_command(name="queue-remove", aliases=["qr"])
    async def queue_remove(self, ctx: BridgeContext):
        """
        Remove yourself from the queue.
        """
        user_id = ctx.author.id
        if not self.database.delete_user_from_queue(user_id=user_id):
            await ctx.send("You are not in the queue!")
            return
        await ctx.send("You have been removed from the queue!")

    @bridge_command(name="queue-export", aliases=["qe"])
    async def queue_export(self, ctx: BridgeContext):
        """
        Export the queue to a CSV.
        """
        if not self.database.export_user_queue_to_csv("queue.csv"):
            await send_error(ctx=ctx)
            return
        await ctx.send(file=discord.File("queue.csv"))


def setup(bot):
    bot.add_cog(QueueBot(bot))
