import discord
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog is ready")

    @app_commands.command(
        name="dmrole", description="Send a DM to users with a specific role."
    )
    async def dmrole(self, interaction: discord.Interaction, role: discord.Role, message: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You need administrator permissions to use this command.", ephemeral=True
            )
            return

        members = role.members
        if not members:
            await interaction.response.send_message(
                "No members have the specified role.", ephemeral=True
            )
            return

        success_count = 0
        for member in members:
            try:
                await member.send(message)
                success_count += 1
            except discord.Forbidden:
                print(f"Failed to send a message to {member.name} due to privacy settings.")
            except Exception as e:
                print(f"Unexpected error while sending message to {member.name}: {e}")

        await interaction.response.send_message(
            f"Message sent to {success_count} members out of {len(members)}.", ephemeral=True
        )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Admin(bot))
