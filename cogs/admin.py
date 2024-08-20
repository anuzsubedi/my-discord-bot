import discord
from discord.ext import commands
from discord import app_commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog is ready")

    @app_commands.command(
        name="dmrole", description="Send a DM to users with a specific role."
    )
    async def dmrole(self, ctx: discord.Interaction, role: discord.Role, message: str):
        try:
            if ctx.user.guild_permissions.administrator:
                members = role.members
                for member in members:
                    await member.send(message)
                await ctx.response.send_message(
                    f"Sent message to {len(members)} members.", ephemeral=True
                )
            else:
                await ctx.response.send_message(
                    "You need administrator permissions to use this command.",
                    ephemeral=True,
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Admin(bot))
