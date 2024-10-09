import discord
from discord.ext import commands
from utils.dbmanager import DatabaseManager
from discord import app_commands


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    async def is_admin(self, interaction: discord.Interaction):
        """Check if the user is an administrator."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command. Administrator access required.",
                ephemeral=True
            )
            return False
        return True

    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, set_channel_method, channel_type: str):
        """Generic method to set a channel and handle errors."""
        if not await self.is_admin(interaction):
            return

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

    @app_commands.command(
        name="set_mod_roles", description="Set the moderator roles for the server."
    )
    async def set_mod_roles(self, interaction: discord.Interaction, roles: str):
        """Command to set moderator roles for the server."""
        if not await self.is_admin(interaction):
            return

        try:
            role_names = [role.strip() for role in roles.split(",")]  # Split the roles by commas
            self.db_manager.set_mod_roles(interaction.guild.id, role_names)
            await interaction.response.send_message(
                f"Moderator roles set to: {', '.join(role_names)}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while setting the moderator roles.", ephemeral=True
            )
            print(f"An error occurred in set_mod_roles: {e}")

    @app_commands.command(
        name="get_mod_roles", description="Get the moderator roles for the server."
    )
    async def get_mod_roles(self, interaction: discord.Interaction):
        """Command to retrieve moderator roles for the server."""
        if not await self.is_admin(interaction):
            return

        try:
            mod_roles = self.db_manager.get_mod_roles(interaction.guild.id)
            if mod_roles:
                await interaction.response.send_message(
                    f"Moderator roles for this server are: {', '.join(mod_roles)}", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "No moderator roles have been set for this server.", ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while retrieving the moderator roles.", ephemeral=True
            )
            print(f"An error occurred in get_mod_roles: {e}")


async def setup(bot):
    await bot.add_cog(Configuration(bot))
