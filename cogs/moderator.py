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
        try:
            mod_roles = config["configuration"]["mod-roles"]
            for role in ctx.user.roles:
                if role.name in mod_roles:  # Use role.name to compare the role's name
                    return True
            return False

        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

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
                await ctx.response.send_message(
                    "You are eligible to use moderator commands.\nYou are an administrator.",
                    ephemeral=True,
                )
            elif self.check_mod(ctx):
                await ctx.response.send_message(
                    "You are eligible to use moderator commands.\nYou are a moderator.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use moderator commands.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
