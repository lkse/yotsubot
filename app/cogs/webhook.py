import discord
from discord.ext import commands, tasks
from datetime import datetime

import app.logging
import config
import aiohttp


class QuartCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def cog_load() -> None:
        self.session = aiohttp.ClientSession()
        self.channel = self.client.get_channel(1100198629853110312)
        self.message = await channel.fetch_message(1140107257095409664)
        self.status.start()

    async def cog_unload() -> None:
        if self.session is not None:
            await self.session.close()

        self.status.stop()
    
    @tasks.loop(minutes=5, reconnect=True)
    async def status(self) -> None:
        app.logging.logger.info("getting status")
        headers = {"Authorization": f"Bearer {config.Api_Key}"}
        url = "https://api.hyperping.io/v1/monitors"
        async with self.session.get(
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

        if self.message is not None:
            await self.message.edit(embed=embed)
            return

        self.message = await self.channel.send(embed=embed)


def setup(client: commands.Bot) -> None:
    client.add_cog(QuartCog(client))
