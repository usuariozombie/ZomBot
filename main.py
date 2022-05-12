#!/usr/bin/python
# -*- coding: utf-8 -*-

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 🤖 | ZomBot » Datos & Imports
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽

from unicodedata import name
import nextcord, os, json, aiohttp, asyncio
from nextcord.ext import commands
from datetime import datetime

with open("config.json") as jFile:
	data = json.load(jFile)
	jFile.close()
BotPrefix = data["prefix"]
BotToken = data["token"]


ZomTitle = u"""\u001b[31m

       ______ ______  ___ __ __   _______  ______   ______  __     __     
      /_____//_____/\/__//_//_/\/_______/\/_____/\ /_____/\/__/\ /__/\    
      \:::__\\:::_ \ \::\| \| \ \::: _  \ \:::_ \ \\::::_\/\ \::\\:.\ \   
         /: / \:\ \ \ \:.      \ \::(_)  \/\:(_) ) )\:\/___/\_\::_\:_\/   
        /::/___\:\ \ \ \:.\-/\  \ \::  _  \ \: __ `\ \::___\/__\/__\_\_/\ 
       /_:/____/\:\_\ \ \. \  \  \ \::(_)  \ \ \ `\ \ \:\____/\ \ \ \::\ \.
       \_______\/\_____\/\__\/ \__\/\_______\/\_\/ \_\/\_____\/\_\/  \__\/
\u001b[0m"""

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 🤖 | ZomBot » Funciones
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽

if os.name == 'posix':
    _ = os.system('clear')
else:
    _ = os.system('cls')

with open("config.json") as jFile:
    data = json.load(jFile)
    jFile.close()
PREFIX = data["prefix"]
IPKEY = data["ip_key"]
CONFESSIONCHANNEL = data["confession_channel"]
APIKEY = data["api_key"]
BOT_USER_ID = data["bot_user_id"]


print(ZomTitle)


print(f"\u001b[33m[{datetime.now().strftime('%H:%M:%S')} INFO] » Connecting... \u001b[0m\n")

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 🤖 | ZomBot » Código Principal
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽


BotIntents = nextcord.Intents.all()
client = commands.Bot(command_prefix=BotPrefix, intents=BotIntents, case_insensitive=True)
client.remove_command("help")


for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        client.load_extension(f"cogs.{fn[:-3]}")


@client.event
async def on_ready():
    print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} INFO] » ¡Connected! Information about the Discord Bot:\u001b[0m\n")
    print(f"\u001b[33m» {client.user.name}#{client.user.discriminator} ({client.user.id})")
    print(f"\u001b[33m» https://discord.com/api/oauth2/authorize?permissions=8&scope=bot%20applications.commands&client_id={client.user.id}")
    print(f"\u001b[33m» Checking {str(len(client.guilds))} servers connected succesfully with ZomBreX, prefix is {BotPrefix}.")


@client.event
async def on_raw_reaction_add(payload):
		if payload.member.id != client.user.id and str(payload.emoji) == u"\U0001F3AB":
			msg_id, channel_id, category_id = client.ticket_configs[payload.guild_id]

			if payload.message_id == msg_id:
				guild = client.get_guild(payload.guild_id)

				for category in guild.categories:
					if category.id == category_id:
						break

				channel = guild.get_channel(channel_id)

				ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}", topic=f"Ticket de {payload.member.display_name}.")

				await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True, read_message_history=True)

				message = await channel.fetch_message(msg_id)
				await message.remove_reaction(payload.emoji, payload.member)

				await ticket_channel.send(f"{payload.member.mention} ¡Gracias por crear un ticket! Usa **'-close'** para cerrar tu ticket.")

				try:
					await client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close", timeout=3600)

				except asyncio.TimeoutError:
					await ticket_channel.delete()

				else:
					await ticket_channel.delete()


# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 🤖 | ZomBot » Cog commands
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Se ha cargado la cog.")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Se ha desactivado la cog.")


@client.command()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    await ctx.send("Se ha recargado la cog.")

async def startup():
    client.session = aiohttp.ClientSession()

client.loop.create_task(startup())


client.run(BotToken)