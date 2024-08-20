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

    def check_mod(self, ctx):
        mod_roles = config["configuration"]["mod-roles"]
        for role in ctx.user.roles:
            if role in mod_roles:
                return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderator Cog is ready")

    @app_commands.command(
        name="checkmod", description="A command to check moderator permissions."
    )
    async def checkmod(self, ctx: discord.Interaction):
        try:
            mod_roles = config["configuration"]["mod-roles"]
            if ctx.user.guild_permissions.administrator:
                await ctx.response.send_message("You are an administrator.")
            elif self.check_mod(ctx):
                await ctx.response.send_message("You are a moderator.")
            else:
                await ctx.response.send_message("You are not a moderator.")
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
