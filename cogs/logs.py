import discord
from discord.ext import commands
import os


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_ID = bot.config["LOGS_CHANNEL_ID"]
        self.logs_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs_channel = self.bot.get_channel(self.log_ID)
        print(f"{os.path.basename(__file__)} loaded")

    # FIX BEFORE + AFTER FIELDS CAN'T BE MORE THAN 1024 - trim code
    
    # def clamp_field(text: str, limit: int = 1024) -> str:
    #   if not text:
    #       return "*[empty]*"
    # Discord embed field values must be <= 1024
    #   if len(text) <= limit:
    #       return text
    # leave room for ellipsis
    #   return text[: limit - 3] + "..."

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        embed = discord.Embed(title="DELETE", description=f"**{message.author.name} deleted a message in {message.channel.mention}**", color=0xFF0000)
        embed.add_field(name="Old Content:", value=f"{message.content}", inline=True)
        await self.logs_channel.send(embed=embed)
        for attachements in message.attachments:
            await self.logs_channel.send(f"Attachment: \n {attachements}")

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if (message_before.content != message_after.content):
            embed = discord.Embed(title="EDIT", description=f"**{message_before.author.name} edited a message in {message_before.channel.mention}**", color=0x00bbff)
            embed.add_field(name="Before:", value=message_before.content, inline=True)
            embed.add_field(name="After:", value=message_after.content, inline=True)
            await self.logs_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logs(bot))
