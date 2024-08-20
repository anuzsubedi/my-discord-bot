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

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator perms."
    )
    async def testmod(self, interaction: discord.Interaction):

        mod_roles = config["configuration"]["mod-roles"]
        if mod_roles is None:
            await interaction.response.send_message(
                f"This is a moderator command.\nNo moderator roles are configured."
            )
            return
        if (
            any(role in mod_roles for role in interaction.user.roles)
            or interaction.user.guild_permissions.administrator
        ):
            await interaction.response.send_message("You have moderator permissions.")
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.",
            )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
