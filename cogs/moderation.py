import nextcord, json, random, asyncio, humanfriendly
from nextcord.ext import commands
from global_functions import ban_msg, kick_msg
from datetime import datetime, timedelta
from main import BOT_USER_ID
from nextcord.ext.commands import errors



class BanConfirm(nextcord.ui.View):
    async def interaction_check(self,interaction):
        if self.ctx.author != interaction.user:
            await interaction.response.send_message('Not your message', ephemeral=True)
            return False
        return True
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
    def __init__(self,ctx,**kwargs):
        super().__init__(timeout=60,**kwargs)
        self.value = None
        self.ctx = ctx

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()



class Moderation(commands.Cog):

    """Some moderation commands."""
    
    COG_EMOJI = "🔨"


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.command(help="🚓 - Bans the member from your server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Member to ban - Not Found"
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Can not ban yourself, trust me I woulda ages ago",
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.red(),
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banMsg = random.choice(ban_msg)
        banEmbed = nextcord.Embed(
            description=f"{member.mention} {banMsg} Reason: {reason}", color=nextcord.Color.red()
        )
        banEmbed.set_author(name=f"{ctx.bot.user.name} · Ban Successful!", icon_url=ctx.guild.icon)
        await ctx.send(embed=banEmbed)
        await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no ban permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(help="🆓 - Unbans a member from your server by ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        em = nextcord.Embed(description=f"You have unbanned <@{id}>")
        em.set_author(name=f"{ctx.bot.user.name} · Unban Successful!", icon_url=ctx.guild.icon)
        await ctx.send(embed=em)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no unban permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(help="🚪 - Kicks the member from your server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Member to kick - Not Found"
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="I require the ``Kick Members`` permisson to run this command - Missing Permission",
            )
            embed2.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You sadly can't kick yourself.",
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Member **higher** than you in the role hierarchy - Invalid Permission",
            )
            em3.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="Member **higher** than you in the role hierarchy - Invalid Permission"
            )
            em4.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em4)
        guild = ctx.guild
        kickMsg = random.choice(kick_msg)
        kickEmbed = nextcord.Embed(
            color=nextcord.Color.random(),
            description=f"{member.mention} {kickMsg} **Reason:** {reason}"
        )
        kickEmbed.set_author(name=f"{ctx.bot.user.name} · Kick Successful! ", icon_url=ctx.guild.icon)
        await ctx.send(embed=kickEmbed)
        await member.send(f"You got kicked in **{guild}** | Reason: **{reason}**")
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no kick permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help="🗑️ - Clears a bundle of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        if amount > 101:
            em1 = nextcord.Embed(
                description="Purge limit exedeed - Greater than 100",
            )
            em1.set_author(name=f"{ctx.bot.user.name} · Clear Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em1)
        else:
            await ctx.channel.purge(limit=amount)
            msg = nextcord.Embed(
            )
            msg.set_author(name=f"{ctx.bot.user.name} · Clear Successful! ", icon_url=ctx.guild.icon)
            msg.set_footer(text=f"Clear requested by {ctx.author}")
            await ctx.send(embed=msg)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no clear permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help="🐢 - Change the channels slowmode.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        try:
            if time == 0:
                em1 = nextcord.Embed(
                    description="Slowmode turned off"
                )
                em1.set_author(name=f"{ctx.bot.user.name} · Slowmode", icon_url=ctx.guild.icon)
                await ctx.send(embed=em1)
                await ctx.channel.edit(slowmode_delay=0)
            elif time > 21600:
                em2 = nextcord.Embed(
                    description="Slowmode over 6 hours"
                )
                em2.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em2)
            else:
                await ctx.channel.edit(slowmode_delay=time)
                em3 = nextcord.Embed(
                    description=f"Slowmode set to {time} seconds",
                )
                em3.set_author(name=f"{ctx.bot.user.name} · Slowmode", icon_url=ctx.guild.icon)
                await ctx.send(embed=em3)
        except Exception:
            await ctx.send("Error has occurred, notifying dev team")
            print(Exception)

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no slowmode permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(aliases=["giverole", "addr"], help="➕ - Gives a member a certain role.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                description="Please mention an user to give them a role!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                description="Please mention a role to give {} that role!".format(
                    member.mention
                ),
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                description="You do not have enough permissions to give this role",
            )
            em.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                description="That role is too high for me to perform this action",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    description=f"{member.mention} already has the role you are trying to give",
                )
                embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                em.set_author(name=f"{ctx.bot.user.name} · Role Added!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no addrole permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(aliases=["takerole", "remover"], help="➖ - Removes a certain role from a member.",)
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                description="Please mention an user to remove a role from them!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                description="Please mention a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                description="You do not have enough permissions to remove this role",
            )
            em.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                description="That role is too high for me to perform this action",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed)
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    break
            if not roleRemoved:
                embed = nextcord.Embed(
                    description=f"{member.mention} already has the role you are trying to give",
                )
                embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                em.set_author(name=f"{ctx.bot.user.name} · Role Removed!", icon_url=ctx.guild.icon)
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)

    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no removerole permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Moderation enabled.\u001b[0m")
    

    
    @commands.command(help = "🔇 - Mute members with this command.")
    async def mute(self, ctx, member: nextcord.Member, time=None, reason=None):
        if member == None:
            embed = nextcord.Embed(
                description="Please mention an user to mute them!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if time == None:
            embed = nextcord.Embed(
                description="Please specify a time to mute them for!",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < member.top_role.position:
            em = nextcord.Embed(
                description="You do not have enough permissions to mute this member",
            )
            em.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em)
        else:
            time = humanfriendly.parse_timespan(time)
            await member.edit(timeout=nextcord.utils.utcnow() + timedelta(seconds=time))
            await member.send(f"You got muted in {ctx.guild} | Reason: {reason}")
            embed = nextcord.Embed(
                description=f"{member.mention} has been muted for {time}",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Muted!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no mute permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)


    @commands.command(help = "🔊 - Unmute members with this command.")
    async def unmute(self, ctx, member: nextcord.Member, reason=None):
        if member == None:
            await ctx.send("Please mention a user to mute!")
        else:
            await member.edit(timeout=None)
            await member.send(f"You got unmuted in {ctx.guild} | Reason: {reason}")
            embed = nextcord.Embed(
                description=f"{member.mention} has been unmuted",
            )
            embed.set_author(name=f"{ctx.bot.user.name} · Unmuted!", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)
            return

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no unmute permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)

    @commands.command(help = "🎚️ - Enable or disable the different commands with this command.")
    async def switch(self, ctx, *, command):
        if not ctx.author.id == 200391563346575361:
            await ctx.reply("Don't even try POGGERS.")
            return
        command = self.get_command(command)
        if command == None:
            await ctx.reply("Couldn't find that command **SADGE**.")
        elif ctx.command == command:
            await ctx.send("You cannot disable this command dude lol poggers.")
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send (f"The {command.qualified_name} command has been {ternary}")
    
    
    @commands.command(help = "🚔 - Ban command for moderators.")
    @commands.has_permissions(kick_members=True)
    async def modban(self, ctx, member: nextcord.Member, *, reason=None):
        if reason is None:
            reason = f"{ctx.author.name} modbanned {member.name}"
        else:
            reason = (
                f"{ctx.author.name} modbanned {member.name} for the reason of {reason}"
            )
        if member == None:
            embed1 = nextcord.Embed(
                description="Member not found!"
            )
            embed1.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                description="Sorry, you cannot ban yourself"
            )
            embed69.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed69)
        if ctx.author.top_role.position <= member.top_role.position:
            embed2 = nextcord.Embed(
                description="You cannot ban someone with a higher role than you!"
            )
            embed2.set_author(name=f"{ctx.bot.user.name} · Error!", icon_url=ctx.guild.icon)
            return await ctx.send(embed=embed2)
        em = nextcord.Embed(
            description=f"**Are you sure you want to ban {member}?**\nThis action cannot be undone and should just be used in special cases"
        )
        em.set_author(name=f"{ctx.bot.user.name} · Are you sure?", icon_url=ctx.guild.icon)
        view = BanConfirm(ctx)
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command timed out, try again later.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                description=f"{member.mention} {banMsg} | Reason: {reason}"
            )
            banEmbed.set_author(name=f"{ctx.bot.user.name} · Banned!", icon_url=ctx.guild.icon)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                description="Your ban has been cancelled"
            )
            banEmbed.set_author(name=f"{ctx.bot.user.name} · Ban Cancelled!", icon_url=ctx.guild.icon)
            await ctx.author.send(embed=banEmbed)

    @modban.error
    async def modban_error(self, ctx, error):
        if isinstance(error, errors.MissingPermissions):
            em5 = nextcord.Embed(
                color=nextcord.Color.random(),
                description="You have no ban permisions :face_with_raised_eyebrow: - Invalid Permission"
            )
            em5.set_author(name=f"{ctx.bot.user.name} · Error! ", icon_url=ctx.guild.icon)
            return await ctx.send(embed=em5)



def setup(client):
    client.add_cog(Moderation(client))