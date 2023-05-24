import discord
from bot import WelcomeBot
from discord.ext import commands


class WelcomeCmds(commands.Cog):
    def __init__(self, bot: WelcomeBot):
        self.bot = bot


async def setup(bot: WelcomeBot):
    await bot.add_cog(WelcomeCmds(bot))