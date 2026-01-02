import discord
from discord.ext import commands
from discord import app_commands
from services import cog_service
import os


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} loaded")

    @app_commands.command(name="ping", description="Test the ping of the bot")
    @app_commands.default_permissions(moderate_members=True)
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Pong {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="reload", description="Reload a cog | Ex: /reload [cog]")
    @app_commands.default_permissions(moderate_members=True)
    async def reload(self, interaction: discord.Interaction, cog: str) -> None:
        await cog_service.unload(self.bot, cog)
        await cog_service.load(self.bot, cog)
        await interaction.response.send_message(f"Reloaded {cog}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
