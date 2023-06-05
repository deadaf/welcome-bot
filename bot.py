import discord
from discord.ext import commands
import config
import asyncpg


exts = ["cogs.dev", "cogs.welcome"]


class WelcomeBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        try:
            self.db = await asyncpg.create_pool(
                config.DB_CONFIG, min_size=4, max_size=5
            )
            print("Connected to database.")

        except Exception as e:
            print("Failed to connect to database. {0}".format(e))

        with open("schemas.sql") as f:
            await self.db.execute(f.read())

        print("Executed all queries.")

        for ext in exts:
            await self.load_extension(ext)

        print("Loaded all cogs.")

    async def on_ready(self):
        print(f"{self.user} ({self.user.id}) is online!")


if __name__ == "__main__":
    bot = WelcomeBot(command_prefix="!", intents=discord.Intents.all())
    bot.run(config.DISCORD_TOKEN)
