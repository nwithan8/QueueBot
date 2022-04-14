from discord.ext.commands import Cog

from modules.utils import int_to_place, DynamicClassCreator
from queue_bot_configuration import QueueBotConfig
from queues.queue_bot_users import QueueBotUsers


def setup(bot):
    config = QueueBotConfig(config_files=["queue_bot_config.yaml"])

    queues = [
        QueueBotUsers
    ]

    creator = DynamicClassCreator()
    cog_class = creator(queues)
    bot.add_cog(cog_class(bot))
