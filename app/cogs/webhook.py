import discord
from discord.ext import commands, tasks
from datetime import datetime

import app.logging
import config
import aiohttp


class QuartCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=5, reconnect=True)
    async def status(self):
        app.logging.logger.info("getting status")
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

        embed.set_footer(text="yotsubot, by lkse", icon_url=self.client.user.avatar.url)

        channel = self.client.get_channel(1100198629853110312)
        if channel:
            msg = await channel.fetch_message(1140107257095409664)
            if msg:
                await msg.edit(embed=embed)
            else:
                await channel.send(embed=embed)


def setup(client):
    cog = QuartCog(client)
    client.add_cog(cog)
    cog.status.start()
