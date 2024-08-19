import datetime
import discord
from discord.ext import commands
import yaml

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
        description = f"Welcome {member.mention} to the server!\n\nPlease familiarize yourself with the rules and enjoy your stay!"
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

        # Calculate the time the member was in the server
        current_time = datetime.now(datetime.timezone.utc)
        join_time = member.joined_at

        # Calculate the difference
        time_difference = current_time - join_time

        # Break down the time difference into years, days, hours, and minutes
        years, remainder = divmod(time_difference.total_seconds(), 365 * 24 * 3600)
        days, remainder = divmod(remainder, 24 * 3600)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        # Format the output based on the largest relevant time unit
        if years >= 1:
            left_after = f"{int(years)} years, {int(days)} days"
        elif days >= 1:
            left_after = f"{int(days)} days, {int(hours)} hours"
        elif hours >= 1:
            left_after = f"{int(hours)} hours and {int(minutes)} minutes"
        else:
            left_after = f"{int(minutes)} minutes"

        # Create the embed message
        embed = discord.Embed(
            title="Member Left",
            description=f"Goodbye {member.mention}!\n\nWe hope to see you again soon!",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"{member.name} was here for {left_after}")

        # Send the embed message
        await join_leave_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logger(bot))
