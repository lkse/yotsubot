import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Sends the Bots Latency")
    async def ping(self, ctx):
        await ctx.respond(f"Latency: {round(self.client.latency*100)}ms")


def setup(client):
    client.add_cog(Ping(client))
