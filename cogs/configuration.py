import discord
from discord.ext import commands
from utils.dbmanager import DatabaseManager
from discord import app_commands


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    @app_commands.command(
        name="set_announcement_channel", description="Set the announcement channel."
    )
    async def set_announcement_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Command to set the announcement channel."""
        try:
            self.db_manager.set_announcement_channel(interaction.guild.id, channel.id)
            await interaction.response.send_message(
                f"Announcement channel set to {channel.mention}.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I do not have permission to send messages in that channel.", ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"Failed to send message due to network issues: {e}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while setting the announcement channel.", ephemeral=True
            )
            print(f"An unexpected error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Configuration(bot))
