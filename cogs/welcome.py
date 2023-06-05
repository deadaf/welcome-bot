import discord
from bot import WelcomeBot
from discord.ext import commands
from discord import app_commands
from utils.wel import get_welcome_card


class WelcomeCmds(commands.Cog):
    def __init__(self, bot: WelcomeBot):
        self.bot = bot

    welcome = app_commands.Group(
        name="welcome", description="Welcome commands", guild_only=True
    )

    @welcome.command(name="channel", description="Set the welcome channel")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await self.bot.db.execute(
            "INSERT INTO welcome (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = $2",
            interaction.guild.id,
            channel.id,
        )
        await interaction.response.send_message(
            f"Set welcome channel to {channel.mention}"
        )

    @welcome.command(name="message", description="Set the welcome message")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_message(self, interaction: discord.Interaction, *, message: str):
        check = await self.bot.db.fetchrow(
            "SELECT * FROM welcome WHERE guild_id = $1", interaction.guild.id
        )
        if not check:
            return await interaction.response.send_message(
                "Please set a welcome channel first!"
            )

        await self.bot.db.execute(
            "UPDATE welcome SET message = $1 WHERE guild_id = $2",
            message,
            interaction.guild.id,
        )
        await interaction.response.send_message(f"Set welcome message to {message}")

    @welcome.command(name="test", description="Test the welcome message")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def test(self, interaction: discord.Interaction, user: discord.Member):
        self.bot.dispatch("member_join", user)
        return await interaction.response.send_message("Sent test message!")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        record = await self.bot.db.fetchrow(
            "SELECT * FROM welcome WHERE guild_id = $1", member.guild.id
        )
        if not record:
            return

        channel = member.guild.get_channel(record["channel_id"])
        message = record["message"]

        welcome_card = await get_welcome_card(member)

        await channel.send(
            message.format(user=member, guild=member.guild.name),
            file=discord.File(welcome_card, filename="welcome.png"),
        )


async def setup(bot: WelcomeBot):
    await bot.add_cog(WelcomeCmds(bot))
