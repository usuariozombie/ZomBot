import nextcord, json, random, asyncio, humanfriendly
from nextcord.ext import commands
from global_functions import ban_msg, kick_msg
from datetime import datetime, timedelta
from main import BOT_USER_ID



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
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Can not ban yourself, trust me I woulda ages ago",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banMsg = random.choice(ban_msg)
        banEmbed = nextcord.Embed(
            title="Ban Success", description=f"{member.mention} {banMsg}"
        )
        banEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=banEmbed)
        await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        await member.ban(reason=reason)

    @commands.command(help="🆓 - Unbans a member from your server by ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        em = nextcord.Embed(title="Unban Success", description=f"You have unbanned <@{id}>")
        await ctx.send(embed=em)

    @commands.command(help="🚪 - Kicks the member from your server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Kick Error", description="Member to kick - Not Found"
            )
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                title="Kick Error",
                description="I require the ``Kick Members`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Kick Error",
                description="You sadly can not kick your self <a:sadboi:795385450978213938>",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        kickMsg = random.choice(kick_msg)
        kickEmbed = nextcord.Embed(
            title="Kick Success", description=f"{member.mention} {kickMsg}"
        )
        kickEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=kickEmbed)
        await member.send(f"You got kicked in **{guild}** | Reason: **{reason}**")
        await member.kick(reason=reason)


    @commands.command(help="🗑️ - Clears a bundle of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        if amount > 101:
            em1 = nextcord.Embed(
                title="Clear Error",
                description="Purge limit exedeed - Greater than 100",
            )
            return await ctx.send(embed=em1)
        else:
            await ctx.channel.purge(limit=amount)
            msg = await ctx.send("Cleared Messages")
            asyncio.sleep(10)
            await msg.delete()

    @commands.command(help="🐢 - Change the channels slowmode.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        try:
            if time == 0:
                em1 = nextcord.Embed(
                    title="Slowmode Success", description="Slowmode turned off"
                )
                await ctx.send(embed=em1)
                await ctx.channel.edit(slowmode_delay=0)
            elif time > 21600:
                em2 = nextcord.Embed(
                    title="Slowmode Error", description="Slowmode over 6 hours"
                )
                await ctx.send(embed=em2)
            else:
                await ctx.channel.edit(slowmode_delay=time)
                em3 = nextcord.Embed(
                    title="Slowmode Success",
                    description=f"Slowmode set to {time} seconds",
                )
                await ctx.send(embed=em3)
        except Exception:
            await ctx.send("Error has occoured, notifying dev team")
            print(Exception)

    @commands.command(aliases=["giverole", "addr"], help="➕ - Gives a member a certain role.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a user to give them a role!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a role to give {} that role!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Add Role Error",
                description="You do not have enough permissions to give this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    title="Add Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Add Role Success",
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

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
                title="Remove Role Error",
                description="Please ping a user to remove a role from them!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Remove Role Error",
                description="You do not have enough permissions to remove this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="That role is too high for me to perform this action",
            )
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
                    title="Remove Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Remove Role Success!",
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} MODULE] » Moderation enabled.\u001b[0m")
    

    
    @commands.command(help = "🔇 - Mute members with this command.")
    async def mute(self, ctx, member: nextcord.Member, time=None, reason=None):
        if member == None:
            await ctx.send("Please mention a user to mute!")
        if time == None:
            await ctx.send("Please specify a time to mute the user for!")
        else:
            time = humanfriendly.parse_timespan(time)
            await member.edit(timeout=nextcord.utils.utcnow() + timedelta(seconds=time))
            await member.send(f"You got muted in {ctx.guild} | Reason: {reason}")
            await ctx.send(f"{member.mention} has been muted for {humanfriendly.format_timespan(time)} | Reason: {reason}")


    @commands.command(help = "🔊 - Unmute members with this command.")
    async def unmute(self, ctx, member: nextcord.Member, reason=None):
        if member == None:
            await ctx.send("Please mention a user to mute!")
        else:
            await member.edit(timeout=None)
            await ctx.send(f"{member.mention} has been muted for {reason}")


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
                title="Ban Error", description="Member not found!"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Sorry, you cannot ban yourself"
            )
            return await ctx.send(embed=embed69)
        em = nextcord.Embed(
            title="Are you sure?",
            description=f"**Are you sure you want to ban {member}?**\nThis action cannot be undone and should just be used in special cases"
        )
        view = BanConfirm(ctx)
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command timed out, try again later.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                title="Ban Success", description=f"{member.mention} {banMsg}"
            )
            banEmbed.add_field(name="Reason", value=reason)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                title="Ban Cancelled",
                description="Your ban has been cancelled"
            )
            await ctx.author.send(embed=banEmbed)



def setup(client):
    client.add_cog(Moderation(client))