import discord
from discord.ext import commands
from utils.dbmanager import DatabaseManager
from discord import app_commands


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, set_channel_method, channel_type: str):
        """Generic method to set a channel and handle errors."""
        try:
            set_channel_method(interaction.guild.id, channel.id)
            await interaction.response.send_message(
                f"{channel_type} channel set to {channel.mention}.", ephemeral=True
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
                f"An error occurred while setting the {channel_type} channel.", ephemeral=True
            )
            print(f"An unexpected error occurred: {e}")

    @app_commands.command(
        name="set_announcement_channel", description="Set the announcement channel."
    )
    async def set_announcement_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Command to set the announcement channel."""
        await self.set_channel(interaction, channel, self.db_manager.set_announcement_channel, "Announcement")

    @app_commands.command(
        name="set_join_leave_channel", description="Set the join-leave log channel."
    )
    async def set_join_leave_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Command to set the join-leave log channel."""
        await self.set_channel(interaction, channel, self.db_manager.set_join_leave_channel, "Join-Leave")

    @app_commands.command(
        name="set_log_channel", description="Set the log channel."
    )
    async def set_log_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Command to set the log channel."""
        await self.set_channel(interaction, channel, self.db_manager.set_log_channel, "Log")

    @app_commands.command(
        name="set_member_detail_channel", description="Set the member detail log channel."
    )
    async def set_member_detail_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Command to set the member detail log channel."""
        await self.set_channel(interaction, channel, self.db_manager.set_member_detail_channel, "Member Detail")


async def setup(bot):
    await bot.add_cog(Configuration(bot))
