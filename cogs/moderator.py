import discord
from discord.ext import commands
from discord import app_commands
import utils.dbmanager as db


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = db.DatabaseManager()

    def check_mod(self, ctx):
        """Check if the user has a moderator role."""
        try:
            mod_roles = self.db_manager.get_mod_roles(ctx.guild.id)  # Fetch mod roles from the database
            return any(role.name in mod_roles for role in ctx.user.roles)
        except Exception as e:
            print(f"Error checking mod roles: {e}")
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator permissions."
    )
    async def checkmod(self, interaction: discord.Interaction):
        """Check if the user has moderator permissions."""
        try:
            if interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "You are eligible to use moderator commands. You are an administrator.",
                    ephemeral=True,
                )
            elif self.check_mod(interaction):
                await interaction.response.send_message(
                    "You are eligible to use moderator commands. You are a moderator.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "You are not allowed to use moderator commands.",
                    ephemeral=True,
                )
        except Exception as e:
            print(f"Error in checkmod command: {e}")

    @app_commands.command(
        name="announce", description="Send an announcement to the announcement channel."
    )
    async def announce(self, interaction: discord.Interaction, message: str):
        """Send an announcement to the announcement channel."""
        try:
            message = message.replace("\\n", "\n")

            if interaction.user.guild_permissions.administrator or self.check_mod(interaction):
                announcement_channel_id = self.db_manager.get_announcement_channel(interaction.guild.id)

                if not announcement_channel_id:
                    await interaction.response.send_message(
                        "Announcement channel not found in the database.",
                        ephemeral=True,
                    )
                    return

                announcement_channel = self.bot.get_channel(announcement_channel_id)

                if not announcement_channel:
                    await interaction.response.send_message(
                        "Announcement channel not found in the guild.",
                        ephemeral=True,
                    )
                    return

                await announcement_channel.send(message)
                await interaction.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "You are not allowed to use this command.",
                    ephemeral=True,
                )

        except Exception as e:
            print(f"Error in announce command: {e}")

    @app_commands.command(
        name="embedannounce", description="Send an announcement as an embed."
    )
    async def embed_announce(self, interaction: discord.Interaction, title: str, description: str):
        """Send an announcement as an embed to the announcement channel."""
        try:
            if interaction.user.guild_permissions.administrator or self.check_mod(interaction):
                announcement_channel_id = self.db_manager.get_announcement_channel(interaction.guild.id)

                if not announcement_channel_id:
                    await interaction.response.send_message(
                        "Announcement channel not found in the database.",
                        ephemeral=True,
                    )
                    return

                announcement_channel = self.bot.get_channel(announcement_channel_id)

                if not announcement_channel:
                    await interaction.response.send_message(
                        "Announcement channel not found in the guild.",
                        ephemeral=True,
                    )
                    return

                embed = discord.Embed(
                    title=title,
                    description=description.replace("\\n", "\n"),
                    color=discord.Color.green(),
                )
                await announcement_channel.send(embed=embed)
                await interaction.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "You are not allowed to use this command.",
                    ephemeral=True,
                )

        except Exception as e:
            print(f"Error in embedannounce command: {e}")

    @app_commands.command(
        name="sendbotmessage",
        description="Send a message as the bot in specified channel.",
    )
    async def send_bot_message(
        self, interaction: discord.Interaction, channel: discord.TextChannel, message: str
    ):
        """Send a message as the bot in a specified channel."""
        try:
            if interaction.user.guild_permissions.administrator or self.check_mod(interaction):
                await channel.send(message.replace("\\n", "\n"))
                await interaction.response.send_message(
                    f"Message sent to {channel.mention}.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"Error in sendbotmessage command: {e}")

    @app_commands.command(
        name="sendbotembed",
        description="Send an embed message as the bot in specified channel.",
    )
    async def send_bot_embed(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        description: str,
    ):
        """Send an embed message as the bot in a specified channel."""
        try:
            if interaction.user.guild_permissions.administrator or self.check_mod(interaction):
                embed = discord.Embed(
                    title=title,
                    description=description.replace("\\n", "\n"),
                    color=discord.Color.green(),
                )
                await channel.send(embed=embed)
                await interaction.response.send_message(
                    f"Embed message sent to {channel.mention}.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"Error in sendbotembed command: {e}")

    @app_commands.command(
        name="purgeall", description="Delete up to 1000 messages in the channel."
    )
    async def purge_all(self, interaction: discord.Interaction):
        """Delete up to 1000 messages in the channel."""
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        try:
            await interaction.response.defer(ephemeral=True)
            deleted = await interaction.channel.purge(limit=1000)
            await interaction.followup.send(
                f"Successfully deleted {len(deleted)} messages.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "I do not have permission to delete messages in this channel.",
                ephemeral=True,
            )

    @app_commands.command(
        name="purge", description="Delete a specific number of messages in the channel."
    )
    async def purge(self, interaction: discord.Interaction, amount: int):
        """Delete a specific number of messages in the channel."""
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        try:
            await interaction.response.defer(ephemeral=True)
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(
                f"Successfully deleted {len(deleted)} messages.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "I do not have permission to delete messages in this channel.",
                ephemeral=True,
            )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
