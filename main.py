import discord
from discord.ext import commands
import app
import config

client = commands.Bot(intents=config.Intents)
for cog in app.cogs:
    client.load_extension(f"app.cogs.{cog}")


@client.event
async def on_ready():
    await client.sync_commands()
    app.logging.logger.info(f"""
    Logged in as {client.user.name}, ID: ({client.user.id})
    Guilds: {len(client.guilds)}
    Users: {len(client.users)}
    Latency: {round(client.latency * 100)}ms
    Commands: {len(client.application_commands)}
    Cogs: {len(client.cogs)}
    """)


@client.event
async def on_error(event):
    app.logging.logger.error(event)


@client.event
async def on_connect():
    app.logging.logger.info(f"""
    {client.user} Connected to Discord
    ID: {client.user.id}
    """)


@client.event
async def on_disconnect():
    app.logging.logger.warn(f"""
    {client.user} Disconnected, Or Connection Attempt Failed.
    """)


@client.event
async def on_resume():
    app.logging.logger.info(f"""
    Session Resumed.
    """)

if __name__ == "__main__":
    app.logging.setup_logging()
    client.run(config.Token)
