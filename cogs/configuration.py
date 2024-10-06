import discord
from discord.ext import commands
from utils.dbmanager import DatabaseManager as db
from discord import app_commands


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = db()

    @app_commands.command(
        name="set_announcement_channel", description="Set the announcement channel."
    )
    async def set_announcement_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        try:
            self.db_manager.set_announcement_channel(interaction.guild.id, channel.id)
            await interaction.response.send_message(
                f"Announcement channel set to {channel.mention}.", ephemeral=True
            )
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Configuration(bot))
