# Queue Bot

A Discord bot to queue items.

# Features

For now, only works to queue users.

Functions:

- `/queue-add`: Adds the user to the queue.
- `/queue-remove`: Removes the user from the queue.
- `/queue-remove @demo_user`: Removes `@demo_user` from the queue (admin-only command).
- `/queue-place`: Say the user's place in the queue.
- `/queue-next`: Get the next user in the queue (admin-only command).
- `/queue-export`: Export the queue to a CSV file (admin-only command).
- `/queue-ping`: Ping the bot to check if it's online.

# Installation

- Clone the repo
- Copy `bot_config.yaml.example` to `bot_config.yaml` and fill it out
- Copy `queue_bot_config.yaml.example` to `queue_bot_config.yaml` and fill it out
- Run the bot with `python3 run.py`