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

    def check_mod(self, interaction: discord.Interaction):
        # Retrieve the moderator role from the configuration
        mod_roles = config["configuration"]["mod-roles"]
        if mod_roles is None:
            interaction.response.send_message(
                f"Moderator roles are not configured.\nThis is a mod command."
            )
            return False
        # Ensure the member has the moderator role
        for role in interaction.user.roles:
            if role.id in mod_roles:
                return True
        return False

    def check_admin(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator perms."
    )
    async def testmod(self, interaction: discord.Interaction):
        if self.check_admin(interaction):
            await interaction.response.send_message(
                "You are an admin and are eligible to use moderator commands",
                ephemeral=True,
            )
        elif self.check_mod(interaction):
            await interaction.response.send_message(
                "You are a moderator and are eligible to use moderator commands",
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
