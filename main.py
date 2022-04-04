#!/usr/bin/python
# -*- coding: utf-8 -*-

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 🤖 | ZomBot » Datos & Imports
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽

from unicodedata import name
import nextcord, os, json, aiohttp
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