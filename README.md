# Queue Bot

A Discord bot to queue items.

# Features

For now, only works to queue users.

Functions:

- `/queue add`: Adds the user to the queue.
- `/queue remove`: Removes the user from the queue.
- `/queue remove @demo_user`: Removes `@demo_user` from the queue (admin-only command).
- `/queue place`: Say the user's place in the queue.
- `/queue next`: Get the next user in the queue (admin-only command).
- `/queue export`: Export the queue to a CSV file (admin-only command).
- `/queue ping`: Ping the bot to check if it's online.

# Installation

1. Clone the repo
2. Copy `bot_config.yaml.example` to `bot_config.yaml` and fill it out
3. Copy `queue_bot_config.yaml.example` to `queue_bot_config.yaml` and fill it out
4. Run the bot with `python3 run.py`

# Red-compatible
There is also a [Red-compatible version](https://github.com/nwithan8/nwithan8-cogs) of this cog, for those using the [Red Discord bot](https://docs.discord.red/en/stable/).
