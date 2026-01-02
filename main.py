import discord
from discord.ext import commands
from data import *
from models import *
from services import *
from utils import *
import json
import os

class AinutaleBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        self._synced = False

        with open("config.json", "r") as config:
            config_data = json.load(config)

        super().__init__(command_prefix=config_data["PREFIX"], intents=intents)
        self.config = config_data
        self.config["LOGS_CHANNEL_ID"] = int(self.config["LOGS_CHANNEL_ID"])

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            try:
                if (filename.endswith(".py")):
                    await self.load_extension(f"cogs.{filename[: -3]}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

    async def on_ready(self):
        if not self._synced:
            await self.tree.sync(guild=self.get_guild(877360002141159425)) #remove guild arg for global sync
            self._synced = True
            print("Slash commands loaded")

        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name =f"{self.command_prefix}help"))
        print(f"Discord.py version: {discord.__version__}")
    
def main():
    bot = AinutaleBot()
    bot.run(bot.config["TOKEN"])

if __name__ == "__main__":
    main()