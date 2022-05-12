import nextcord, aiofiles
from datetime import datetime
from discord.ext import commands
import asyncio


class Tickets(commands.Cog, name="Tickets"):
	"""Allows you to make custom tickets to talk with the server admins."""

	COG_EMOJI = "\U0001F3AB"

	def __init__(self, client):
		self.client = client
		self.client.ticket_configs = {}



	@commands.Cog.listener()
	async def on_ready(self):
		print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » Tickets enabled.\u001b[0m")
		async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
			pass

		async with aiofiles.open("ticket_configs.txt", mode="r") as file:
			lines = await file.readlines()
			for line in lines:
				data = line.split(" ")
				self.client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
	
	@commands.command(help="🎫 - configures the ticketing channel.")
	async def configure_ticket(self, ctx, msg: nextcord.Message=None, category: nextcord.CategoryChannel=None):
		if msg is None or category is None:
			await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
			return

		self.client.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

		async with aiofiles.open("ticket_configs.txt", mode="r") as file:
			data = await file.readlines()

		async with aiofiles.open("ticket_configs.txt", mode="w") as file:
			await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

			for line in data:
				if int(line.split(" ")[0]) != ctx.guild.id:
					await file.write(line)
					
		await msg.add_reaction(u"\U0001F3AB")
		await ctx.channel.send("Succesfully configured the ticket system.")

def setup(client):
    client.add_cog(Tickets(client))