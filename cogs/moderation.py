from discord.ext import commands
import os


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} loaded")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
