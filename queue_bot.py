from discord.ext.commands import Cog

from modules.utils import int_to_place, DynamicClassCreator
from queue_bot_configuration import QueueBotConfig
from queues.queue_bot_items import QueueBotItems
from queues.queue_bot_users import QueueBotUsers

queue_types_to_classes = {
    "user": QueueBotUsers,
    "item": QueueBotItems
}


def setup(bot):
    config = QueueBotConfig(config_files=["queue_bot_config.yaml"])

    queue_classes = []
    for queue_type in config.queue_types:
        queue_class = queue_types_to_classes.get(queue_type, None)
        if queue_class is None:
            raise ValueError(f"Queue type {queue_type} is not supported")
        queue_classes.append(queue_class)

    creator = DynamicClassCreator()
    cog_class = creator(queue_classes)
    bot.add_cog(cog_class(bot))
