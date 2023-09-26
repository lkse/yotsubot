import discord
from discord.ext import commands
import config
import aiohttp
from datetime import datetime
from app import monitor

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
        

        for item in data:
            monitor_instance = getattr(monitor, item['name'])
            for key, value in item.items():
                if key != 'name':
                    setattr(monitor_instance, key, value)
        
        
        embed = discord.Embed(title="Status Page",
                              url="https://status.lks.codes",
                              colour=0x3241c2,
                              timestamp=datetime.now()
                              )

        embed.set_author(name="Kawata Status")

        if monitor.api.status == 'down' and monitor.hanayo.status == 'down' and monitor.peppy.status == 'down':
            service_status = "We are currently experiencing a service outage."
            embed.add_field(name="Summary",
                            value=service_status,
                            inline=False)
        elif monitor.api.status == 'down' or monitor.hanayo.status == 'down' or monitor.peppy.status == 'down':
            service_status = "We are currently experiencing a service disruption."
            embed.add_field(name="Summary",
                            value=service_status,
                            inline=False)

        service_names = ['api', 'hanayo', 'peppy']

        for service_name in service_names:
            service = getattr(monitor, service_name)
            

            status_text = "Down" if service.status == 'down' else "Up"
            embed.add_field(name=service_name, value=status_text, inline=True)

        embed.set_footer(text="yotsubot, by lkse",
                         icon_url=self.client.user.avatar.url)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Status(client))
