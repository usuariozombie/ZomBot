from click import command
import nextcord, asyncio
from nextcord.ext import commands
from datetime import datetime
from nextcord import message
from afks import afks
from nextcord.utils import get


class AFK(commands.Cog):

    """Sets your status to AFK."""

    def __init__(self, client):
        self.client = client

    COG_EMOJI = "💤"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » AFK's enabled.\u001b[0m")

    @commands.command(help = "😴 - Sets your status to AFK.")
    async def afk(self,ctx,*,reason ="No reason provided"):
        """Go AFK (away from keyboard)"""
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick = f"(AFK) {member.display_name}")
            except:
                pass
        afks[member.id] = reason
        embed = nextcord.Embed(description = f"<:sv_sleepy:869557927764168704>**Reason**: {reason}",color = nextcord.Color.random())
        embed.set_author(name=(f"{ctx.author.name} is now AFK"), icon_url=ctx.author.avatar)
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        def remove(afk):
            if "(AFK)" in afk.split():
                return " ".join(afk.split()[1:])
            else:
                return afk
        
        if message.guild is None:
            return

        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass
            lol = await message.reply(f'Welcome {message.author.name}, you are no longer AFK')
            await asyncio.sleep(5)
            await lol.delete()

        for id, reason in afks.items():
            member = get(message.guild.members, id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                    embed = nextcord.Embed(description = f"<:sv_sleepy:869557927764168704>**Reason**: {reason}",color = nextcord.Color.random())
                    embed.set_author(name=(f"{member.name} is now AFK"), icon_url=member.avatar)
                    embed.set_footer(text=f"{message.guild.name}", icon_url=message.guild.icon)
                    caca = await message.reply(embed=embed)
                    await asyncio.sleep(5)
                    await caca.delete()


def setup(client):
    client.add_cog(AFK(client))