import discord
from discord.ext import commands
from data import *
from models import *
from services import *
from utils import *
import json
import os

intents = discord.Intents.default()
intents.message_content = True

with open("config.json", "r") as config:
    config_data = json.load(config)
    token = config_data["DISCORD_TOKEN"]
    prefix = config_data["PREFIX"]

client = commands.Bot(prefix, intents = intents)

if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        try:
            if (filename.endswith(".py")):
                client.load_extension(f"cogs.{filename[: -3]}")
                print(f"Cog [{filename}] loaded")
        except Exception as e:
            print(f"Failed to load extension {filename}: {e}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name =f"{client.command_prefix}help"))
    print(f"Discord.py version: {discord.__version__}")

client.run(token)