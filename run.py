import discord
from discord.ext import commands, bridge

import credentials
from modules.logs import *

info("Starting application...")

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.ERROR if credentials.SUPPRESS_LOGS else logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = bridge.Bot(credentials.BOT_PREFIX)

formatter = commands.HelpCommand(show_check_failure=False)

extensions = [
    "QueueBot"
]


@bot.event
async def on_ready():
    info(f'\n\nLogged in as : {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Game(
                                  name=f'Making lists, checking them twice | {credentials.BOT_PREFIX}'))
    info(f'Successfully logged in and booted...!\n')


if __name__ == '__main__':
    info("Connecting to Discord...")
    for ext in extensions:
        bot.load_extension(ext)
    bot.run(credentials.DISCORD_BOT_TOKEN)
