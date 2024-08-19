import discord
from discord.ext import commands


class Configure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Configure Cog is ready")

    @discord.app_commands.command(
        name="testconfigure", description="A test configure command"
    )
    async def testconfigure(self, interaction: discord.Interaction):
        await interaction.response.send_message("Configure command is working!")


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Configure(bot))
