import discord
from discord.ext import commands
from discord import app_commands


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(name="testmod", description="A test moderator command")
    async def testmod(self, interaction: discord.Interaction):
        mod_role = discord.utils.get(interaction.guild.roles, name="Moderator")
        if mod_role in interaction.user.roles:
            await interaction.response.send_message("Moderator command is working!")
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
