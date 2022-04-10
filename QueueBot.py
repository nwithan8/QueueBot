from discord.ext import commands

from modules.logs import info
from modules.queue_database import QueueDatabase, UserQueueEntry


class QueueBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = QueueDatabase(sqlite_file="queue.db", table_schemas=[UserQueueEntry])


def setup(bot):
    bot.add_cog(QueueBot(bot))
