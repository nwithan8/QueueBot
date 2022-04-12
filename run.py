import discord
from discord.ext import commands, bridge

from modules.bot_config import BotConfig
from modules.logs import *

info("Starting application...")

bot_config = BotConfig(app_name="QueueBot")

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=bot_config.log_level)

# intents = discord.Intents.default()
# intents.message_content = True
# intents.members = True
intents = discord.Intents(messages=True, members=True, guilds=True)
bot = bridge.Bot(command_prefix=bot_config.bot_prefix, intents=intents)
formatter = commands.HelpCommand(show_check_failure=False)

extensions = [
    "queue_bot"
]


@bot.event
async def on_ready():
    info(f'\n\nLogged in as : {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Game(
                                  name=f'Making lists, checking them twice | {bot_config.bot_prefix}'))
    info(f'Successfully logged in and booted...!\n')


if __name__ == '__main__':
    info("Connecting to Discord...")
    for ext in extensions:
        bot.load_extension(ext)
    bot.run(bot_config.bot_token)
