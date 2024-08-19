import discord
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("User Cog is ready")

    @discord.app_commands.command(name="ping", description="A simple ping command")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(User(bot))
