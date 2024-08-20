import discord
from discord.ext import commands
from discord import app_commands
import yaml

# Load the configuration from the YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_roles = config["configuration"].get("mod-roles", [])

    def is_moderator(self, user: discord.Member) -> bool:
        """Checks if the user has a moderator role."""
        return any(role.id in self.mod_roles for role in user.roles)

    def is_admin(self, user: discord.Member) -> bool:
        """Checks if the user has administrative permissions."""
        return user.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator permissions."
    )
    async def checkmod(self, interaction: discord.Interaction):
        if self.is_admin(interaction.user):
            await interaction.response.send_message(
                "You are an admin and are eligible to use moderator commands.",
                ephemeral=True,
            )
        elif self.is_moderator(interaction.user):
            await interaction.response.send_message(
                "You are a moderator and are eligible to use moderator commands.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You are not a moderator and are not eligible to use moderator commands.",
                ephemeral=True,
            )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
