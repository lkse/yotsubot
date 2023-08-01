import discord
from discord.ext import commands
import app
import config
import logging
import colorlog

import os

logger = logging.getLogger()


def setup_logging():
    """
    Sets up logging for the bot.

    Creates a logger, sets the format, and adds a handler for the console
    with colored output.
    """

    logger.setLevel(logging.INFO)

    logformat = "%(asctime)s %(levelname)-8s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        ))

    logger.addHandler(handler)

    for level in [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG, logging.CRITICAL]:
        filename = f"./logs/{level}.log"
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter(logformat, datefmt))
        logger.addHandler(file_handler)


client = discord.ext.commands.Bot(intents=config.Intents)
client.load_extension('app.cogs.ping')


@client.event
async def on_ready():
    await client.sync_commands()
    logger.info(f"""
    Logged in as {client.user.name}, ID: ({client.user.id})
    Guilds: {len(client.guilds)}
    Users: {len(client.users)}
    Latency: {round(client.latency * 100)}ms
    Commands: {len(client.application_commands)}
    Cogs: {len(client.cogs)}
    """)


if __name__ == "__main__":
    setup_logging()
    client.run(config.Token)
