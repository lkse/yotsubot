import discord
from discord.ext import commands
import config
import aiohttp
from datetime import datetime


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="status", description="Get the Kawata Server status")
    async def status(self, ctx):
        async with ctx.typing():
            headers = {"Authorization": f"Bearer {config.Api_Key}"}
            url = "https://api.hyperping.io/v1/monitors"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                    allow_redirects=True
                ) as resp:
                    data = await resp.json()

        service_names = ["pep.py", "API", "Hanayo"]
        statuses = {name: False for name in service_names}

        for service in data:
            if service["name"] in service_names:
                if service["status"].lower() == "down":
                    statuses[service["name"]] = True

        embed = discord.Embed(title="Status Page",
                              url="https://status.lks.codes",
                              colour=0x3241c2,
                              timestamp=datetime.now()
                              )

        embed.set_author(name="Kawata Status")

        if all(statuses.values()):
            service_status = "We are currently experiencing a service outage."
            embed.add_field(name="Summary",
                            value=service_status,
                            inline=False)
        elif any(statuses.values()):
            service_status = "We are currently experiencing a service disruption."
            embed.add_field(name="Summary",
                            value=service_status,
                            inline=False)

        for service_name in service_names:
            status_text = "Down" if statuses[service_name] else "Up"
            embed.add_field(name=service_name, value=status_text, inline=True)

        embed.set_footer(text="yotsubot, by lkse",
                         icon_url=self.client.user.avatar.url)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Status(client))
