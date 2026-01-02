from discord.ext import commands

async def load(bot: commands.Bot, cog: str) -> None:
    await bot.load_extension(f"cogs.{cog}")

async def unload(bot: commands.Bot, cog: str) -> None:
    await bot.unload_extension(f"cogs.{cog}")