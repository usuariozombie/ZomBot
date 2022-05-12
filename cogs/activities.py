from distutils.log import error
from types import NoneType
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime
from nextcord.ext import activities, commands



class Drowpdown(nextcord.ui.Select):
	def __init__(self, author):
		self.author = author
		selectOptions = [
			nextcord.SelectOption(label="Betrayal.io", description="Multiplayer murder mystery game!", emoji="🗡️"),
			nextcord.SelectOption(label="Fishington", description="An online fishing game where you can relax, chat and fish with up to 24 players!", emoji="🎣"),
			nextcord.SelectOption(label="YoutubeTogether", description="Watch youtube with your friends.", emoji="📺"),
			nextcord.SelectOption(label="Word Snacks", description="Word Snacks is a multiplayer word search game.", emoji="📖"),
			nextcord.SelectOption(label="Sketch Heads", description="In Sketch Heads, players sketch pictures of a word prompt.", emoji="🖼️"),
			nextcord.SelectOption(label="Blazing 8s", description="Crazy Eights-inspired card game that you can play with your friends!", emoji="🃏"),
			nextcord.SelectOption(label="Putt Party", description="It is our putting golf game that you can play with your friends!", emoji="🏌️"),
			nextcord.SelectOption(label="Land.io", description="In Land-io, players claim territory by moving around.", emoji="🗺️"),
			nextcord.SelectOption(label="Poker Night (Tier 1)", description="Texas hold 'em style game mode.", emoji="🎰"),
			nextcord.SelectOption(label="Chess In The Park (Tier 1)", description="Chess multiplayer game.", emoji="♟️"),
			nextcord.SelectOption(label="Checkers In The Park (Tier 1)", description="Checkers multiplayer game.", emoji="♟️"),
			nextcord.SelectOption(label="Spellcase (Tier 1)", description="Spellcasters is a frantic rhythm based combat game.", emoji="🔥"),
			nextcord.SelectOption(label="Letter League (Tier 1)", description="Letter League is a game where you and your friends take turns placing letters on a game board.", emoji="🔤"),
			nextcord.SelectOption(label="Awkword (Tier 1)", description="A fun little game where you create sentences and vote the best sentence with your friends!", emoji="📕"),
		]
		super().__init__(placeholder="Select the activity.", min_values=1, max_values=1, options=selectOptions)

	
	async def callback(self, interaction: Interaction):
		if interaction.user.id == self.author:
			if self.values[0] == "Betrayal.io":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.betrayal)}")
			elif self.values[0] == "Fishington":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.fishington)}")
			elif self.values[0] == "YoutubeTogether":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.watch_together)}")
			elif self.values[0] == "Word Snacks":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.word_snacks)}")
			elif self.values[0] == "Sketch Heads":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.sketch)}")
			elif self.values[0] == "Blazing 8s":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.blazing)}")
			elif self.values[0] == "Putt Party":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.putt_party)}")
			elif self.values[0] == "Land.io":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.land_io)}")
			elif self.values[0] == "Poker Night (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.poker)}")
			elif self.values[0] == "Chess In The Park (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.chess)}")
			elif self.values[0] == "Checkers In The Park (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.checkers)}")
			elif self.values[0] == "Spellcase (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.spellcast)}")
			elif self.values[0] == "Letter League (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.letter_league)}")
			elif self.values[0] == "Awkword (Tier 1)":
				await interaction.response.send_message(f"You chose {self.values[0]}, here is your invite link: {await interaction.user.voice.channel.create_activity_invite(activities.Activity.awkword)}")
			


class DropdownView(nextcord.ui.View):
	def __init__(self, author, timeout):
		self.author = author
		self.timeout = timeout
		super().__init__(timeout=timeout)
		self.add_item(Drowpdown(author))

	async def on_timeout(self):
		await self.message.edit(view=None)

class Socials(commands.Cog, name="Activities"):
	"""Shows a list of activities."""

	COG_EMOJI = "🗃"

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Activities enabled.\u001b[0m")


	@commands.command(name="act", help="🗃 - Select an activity to share with your friends.")
	async def act(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("You must be in a voice channel to use this command.")
		else:
			view = DropdownView(ctx.author.id, 30)
			view.message = await ctx.send("Choose an activity:", view=view)
	    

def setup(client):
	client.add_cog(Socials(client))