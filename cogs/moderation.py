from discord.ext import commands
import os
from discord import app_commands
import discord
from string import Template
import random
from typing import Optional
from pathlib import Path


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} loaded")

    clean_responses = [
        Template("Hey dol! Tom’s tidied away $count little words that cluttered the air!"),
        Template("Tra-la-la! $count wandering messages skipped off down the river."),
        Template("Old Tom swept the leaves away — $count bits of chatter gone!"),
    ]

    @app_commands.command(name="clean", description="Mass delete messages (max: 100) | Ex: /clean 22")
    @app_commands.default_permissions(manage_messages=True)
    async def clean(self, interaction: discord.Interaction, num: app_commands.Range[int, 1, 100], member: Optional[discord.Member]=None) -> None:
        global clean_responses
        curr_channel = interaction.channel
        deleted_count = 0

        if not isinstance(curr_channel, (discord.TextChannel, discord.Thread)):
            return await interaction.followup.send("Tom only tidies text channels and threads!", ephemeral=True)
        
        if member is None:
            deleted_messages = await curr_channel.purge(limit=num)
            deleted_count = len(deleted_messages)
        else:
            def check(msg: discord.Message) -> bool:
                nonlocal deleted_count
                if msg.author.id == member.id:
                    deleted_count += 1
                    return True
                return False
            
            scan_limit = min(2000, num * 50)
            deleted_messages = await curr_channel.purge(limit=scan_limit, check=check)

            # write deleted messages to log file on PC
        
        await interaction.response.send_message(random.choice(clean_responses).substitute(count=num))

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
