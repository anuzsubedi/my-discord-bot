import datetime
import discord
from discord.ext import commands
import yaml
from datetime import datetime
import pytz

# Load the configuration from the YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_leave_channel = self.bot.get_channel(
            config["configuration"]["join-leave-channel"]
        )

        title = "Member Joined"
        description = f"Welcome {member.mention} to the server!\nPlease familiarize yourself with the rules and enjoy your stay!"
        joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M")
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green(),
        )

        embed.set_footer(text=f"Joined at: {joined_at}")

        await join_leave_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Retrieve the join/leave channel from the configuration
        join_leave_channel = self.bot.get_channel(
            config["configuration"]["join-leave-channel"]
        )

        # Ensure the channel is valid
        if join_leave_channel is None:
            return

        # Ensure the member's join date is available
        if member.joined_at is None:
            return

        try:
            left_after = "1 day."
            # Calculate time difference
            joined_at = member.joined_at.astimezone(pytz.UTC)
            now = datetime.now(pytz.UTC)
            difference = now - joined_at

            # Determine time format
            total_seconds = difference.total_seconds()
            days = difference.days
            hours = int(total_seconds // 3600) % 24
            minutes = int(total_seconds // 60) % 60

            if days >= 365:
                years = days // 365
                days_remaining = days % 365
                left_after = f"{years} years. {days_remaining} days."
            elif days > 1:
                left_after = f"{days} days. {hours} hours. {minutes} minutes."
            elif days == 1:
                left_after = f"1 day. {hours} hours. {minutes} minutes."
            elif hours > 0:
                left_after = f"{hours} hours. {minutes} minutes."
            else:
                left_after = f"{minutes} minutes."

            # Create the embed message
            embed = discord.Embed(
                title="Member Left",
                description=f"Goodbye {member.mention}!\nWe hope to see you again soon!",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"{member.name} was here for {left_after}")

            # Send the embed message
            await join_leave_channel.send(embed=embed)
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Logger(bot))
