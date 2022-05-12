import nextcord
from nextcord.ext import commands
from datetime import datetime
from nextcord.ext import commands

logchannel1=900851120161816617
logchannel2=907984748419371058

class Logs(commands.Cog, name="Logs"):
    """This will show deleted and edited messages in a log channel."""

    COG_EMOJI = "📁"

    def __init__(self, client):
        self.client = client
        self.client.sniped_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Logs enabled.\u001b[0m")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel=self.client.get_channel(logchannel1)
        deleted = nextcord.Embed(
            description=f"Message deleted in {message.channel.mention}", color=0x4040EC
        ).set_author(name=message.author, url=nextcord.Embed.Empty, icon_url=message.author.avatar)

        deleted.add_field(name="Message", value=message.content)
        deleted.timestamp = message.created_at
        await channel.send(embed=deleted)
        caca = self.client.get_channel(logchannel2)
        await caca.send(embed=deleted)
        self.client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        embed=nextcord.Embed(description=message_before.channel.mention, color=0x4040EC)
        embed.add_field(name=f"This is the message before", value= message_before.content, inline=False)
        embed.add_field(name=f"This is the message after", value= message_after.content, inline=False)
        embed.set_author(name= message_before.author, icon_url=message_before.author.avatar)
        embed.timestamp = message_after.created_at
        channel=self.client.get_channel(logchannel1)
        caca = self.client.get_channel(logchannel2)
        await channel.send(embed=embed)
        await caca.send(embed=embed)


    @commands.command(help = "🎯 - Shows the last deleted message.")
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.client.sniped_messages[ctx.guild.id]
            
        except:
            await ctx.channel.send(f"No se ha encontrado ningún mensaje reciente en {ctx.channel.mention}")
            return

        embed = nextcord.Embed(description=f"   {contents}", color=nextcord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar)
        embed.set_footer(text=f"Mensaje borrado en: #{channel_name}", icon_url=ctx.guild.icon)

        await ctx.channel.send(embed=embed)

	    

def setup(client):
	client.add_cog(Logs(client))