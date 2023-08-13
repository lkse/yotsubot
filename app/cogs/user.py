import discord
from discord.ext import commands
from datetime import datetime


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="userinfo", description="Gets a provided user's info")
    async def userinfo(self, ctx, user: discord.Member):
        async with ctx.typing():
            embed = discord.Embed(description=f"{user.mention}",
                                  colour=0x3241c2,
                                  timestamp=datetime.now())

            embed.set_author(name=f"{user.name}",
                             icon_url=f"{user.avatar}")

            embed.add_field(name="ID",
                            value=f"{user.id}",
                            inline=True)
            embed.add_field(name="Display Name",
                            value=f"{user.display_name}",
                            inline=True)
            embed.add_field(name="Status",
                            value=f"{user.raw_status}",
                            inline=True)
            embed.add_field(name="Creation Date",
                            value=user.created_at.strftime("%d %B, %Y, %H:%M"),
                            inline=True)
            embed.add_field(name="Join Date",
                            value=user.joined_at.strftime("%d %B, %Y, %H:%M"),
                            inline=True)
            embed.add_field(name="Top Role",
                            value=f"{user.top_role.mention}")
            embed.add_field(name="Roles",
                            value=','.join([role.mention for role in user.roles]))

            embed.set_thumbnail(url=f"{user.display_avatar.url}")

            embed.set_footer(text="yotsubot, by lkse",
                             icon_url=f"{self.client.user.avatar.url}")
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(User(client))
