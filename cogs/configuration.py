import discord
from discord.ext import commands
from utils.dbmanager import DatabaseManager as db
from discord import app_commands

# @app_commands.command(
#         name="testcommand", description="A command to test logging of messaageID"
#     )
#     async def test_command(
#         self, ctx: discord.Interaction, message: str, channel: discord.TextChannel
#     ):
#         try:
#             sentMessage = await channel.send(message)
#             await sentMessage.add_reaction("🔔")
#             await ctx.response.send_message(
#                 f"Messaage sent to {channel.mention}. Message ID: {sentMessage.id}",
#                 ephemeral=True,
#             )
#         except Exception as e:
#             print(f"\n++++++++++++\n")
#             print(e)


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_announcement_channel", description="Set the announcement channel."
    )
    async def set_announcement_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        try:
            # db_manager = db()
            # db_manager.connect_to_mysql()

            # db_manager.close_connection()
            await interaction.response.send_message(
                f"Announcement channel set to {channel.mention}.", ephemeral=True
            )
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Configuration(bot))
