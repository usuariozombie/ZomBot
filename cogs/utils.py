import time, sys, os, nextcord, requests, aiohttp, psutil
from inspect import getsource
from time import time
from datetime import datetime
from nextcord.ext import commands, tasks
from io import BytesIO


us = 0
um = 0 
uh = 0
ud = 0


class Utils(commands.Cog):

    """Some miscellaneous commands."""

    def __init__(self, client):
        self.client = client
        self.clientuptime.start()

    COG_EMOJI = "🧰"

    @commands.command(help = "🧑‍💻 - Shows the user's info.")
    async def userinfo(self, ctx, *, user: nextcord.Member = None):  # b'\xfc'
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_paginator = commands.Paginator(prefix="```diff", max_size=1000)
        for p in user.guild_permissions:
            perm_paginator.add_line(
                f"{'+' if p[1] else '-'} {str(p[0]).replace('_', ' ').title()}"
            )
        embed.add_field(
            name="Guild permissions", value=f"{perm_paginator.pages[0]}", inline=False
        )
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        return await ctx.send(embed=embed)

    @commands.command(help = "🖥️ - Shows the server's information.")
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=ctx.message.created_at, color=ctx.author.color
        )
        embed2.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(
            name="Verification Level",
            value=str(ctx.guild.verification_level),
            inline=True,
        )
        embed2.add_field(name="Highest role", value=ctx.guild.roles[-1], inline=True)
        embed2.add_field(name="Number of roles", value=str(role_count), inline=True)
        embed2.add_field(
            name="Number Of Members", value=ctx.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Created At",
            value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon.url)
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed2.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed2)

    @commands.command(
        aliases=["cs", "ci", "channelinfo"], help = "📈 - Shows the channel's stats."
    )
    async def channelstats(self, ctx, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = ctx.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Category - `{}`'.format(channel.category.name) if channel.category else '`This channel is not in a category`'}",
        )
        embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel Id", value=channel.id, inline=True)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Annoucement", value=channel.is_news(), inline=True)
        embed.add_field(
            name="Channel Permissions", value=channel.permissions_synced, inline=True
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)


    @commands.command(help="🏓 - Shows the ping of the bot")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ping(self, ctx):
        em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
        em.add_field(
            name="My API Latency is:", value=f"{round(self.client.latency*1000)} ms!"
        )
        em.set_footer(
            text=f"Ping requested by {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (
            variable
            if (len(f"{variable}") <= 1000)
            else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>"
        )

    def prepare(self, string):
        arr = (
            string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        )
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(
        pass_context=True,
        aliases=["eval", "exec", "evaluate"],
        help = "✏️ - Evaluates given code",
    )
    async def _eval(self, ctx, *, code: str):
        if not ctx.author.id == 200391563346575361:
            return
        silent = "-s" in code

        code = self.prepare(code.replace("-s", ""))
        args = {
            "nextcord": nextcord,
            "sauce": getsource,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "this": self,
            "ctx": ctx,
            "member": ctx.author,
            "client": self.client,
        }

        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, nextcord.Message):
                em = nextcord.Embed(
                    title="Eval Success :D",
                    description="```Code ran without any errors```",
                )
                await ctx.send(embed=em)
                del args, code
                return
            em = nextcord.Embed(
                title="Eval Success :o",
                description=f"```py\n{self.resolve_variable(response)}```",
            )
            em.set_footer(
                text=f"`{type(response).__name__} | {(time() - a) / 1000} ms`"
            )
            await ctx.send(embed=em)
        except Exception as e:
            em = nextcord.Embed(
                title="Eval Error ._.",
                description=f"```{type(e).__name__}: {str(e)}```",
            )
            await ctx.send(embed=em)

        del args, code, silent

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} MODULE] » Utils enabled.\u001b[0m")

    @commands.command(help = " 😳 - Steals an emoji with the url.")
    async def stealmoji(self, ctx, url:str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.reply("You just stole an emoji lol 🤨")
                        await ses.close()
                    else:
                        await ctx.send(f"Dude, it didn't work so... you'll end up in jail LMAO. {r.status}")
                except nextcord.HTTPException:
                    await ctx.send("Too thicc ass to download dude.")
    
    
    @tasks.loop(seconds=2.0)
    async def clientuptime(self):
        global uh, us, um, ud
        us += 2
        if us == 60:
            us = 0
            um += 1
            if um == 60:
                um = 0
                uh += 1
                if uh == 24:
                    uh = 0
                    ud += 1

    @clientuptime.before_loop
    async def before_clientuptime(self):
        await self.client.wait_until_ready()

    @commands.command(
        help="📟 - Status information for the bot"
    )

    @commands.cooldown(1, 15, commands.BucketType.user)
    async def status(self, ctx):
        global ud, um, uh, us
        em = nextcord.Embed(title="\u200b")
        em.set_author(name=f"VPS Status.", icon_url=ctx.guild.icon)
        em.add_field(name="Days:", value=ud)
        em.add_field(name="Hours:", value=uh)
        em.add_field(name="Minutes:", value=um)
        em.add_field(name="Seconds:", value=us)
        em.add_field(name="CPU usage:", value=f"{psutil.cpu_percent()}%")
        em.add_field(name="RAM usage:", value=f"{psutil.virtual_memory()[2]}%")
        em.set_footer(
            text=f"Status requested by: {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Retry again after {round(error.retry_after, 2)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(876845404786946099):
            send = message.channel.send

    @commands.command(name="sug", help = "📫 - Creates a suggestion in #📫┃𝕊𝕦𝕘𝕖𝕣𝕖𝕟𝕔𝕚𝕒𝕤")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def sug(self, ctx, *, suggestion):
        await ctx.channel.purge(limit = 1)
        channel = nextcord.utils.get(ctx.guild.text_channels, name = '📫┃𝕊𝕦𝕘𝕖𝕣𝕖𝕟𝕔𝕚𝕒𝕤')
        channel2 = nextcord.utils.get(ctx.guild.text_channels, name = 'admin-sugerencias')
        suggest = nextcord.Embed(title=f"Suggestion", description=f"{ctx.message.author} suggests: **{suggestion}**")
        sugg = await channel.send(embed=suggest)
        await channel2.send(f"^^ Suggestion ID: {sugg.id}")
        await sugg.add_reaction('✅')
        await sugg.add_reaction('❌')
    
    @commands.command(name="approve", help = "✅ - Approves a user's suggestion")
    async def approve(self, ctx, id:int=None):
        if id == None:
            em = nextcord.Embed(title='Approve Error', description='Please specify message id')
            return await ctx.send(embed=em)
        channel = nextcord.utils.get(ctx.guild.text_channels, name = '📫┃𝕊𝕦𝕘𝕖𝕣𝕖𝕟𝕔𝕚𝕒𝕤')
        if channel is None:
            embed = nextcord.Embed(title='Approve Error', description='Can not find suggestion channel')
            return await ctx.send(embed=embed)
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(title=f'Suggestion Approved!', description=f'The suggestion id of `{suggestionMsg.id}` has been approved by {ctx.author.mention}')
        await channel.send(embed=embed)




def setup(client):
    client.add_cog(Utils(client))