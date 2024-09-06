import datetime
import discord
from discord.ext import commands
import yaml
from datetime import datetime
import pytz

# Load the configuration from the YAML file
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        isNewUser = False
        # Retrieve the channels from the configuration
        join_leave_channel = self.bot.get_channel(
            config["configuration"]["join-leave-channel"]
        )
        member_details_channel = self.bot.get_channel(
            config["configuration"]["member-detail-log-channel"]
        )

        # Ensure the channels are valid
        if join_leave_channel is None or member_details_channel is None:
            return

        # Calculate account age
        account_creation = member.created_at.astimezone(pytz.UTC)
        now = datetime.now(pytz.UTC)
        account_age_timedelta = now - account_creation
        account_age_days = account_age_timedelta.days
        account_age_hours = int(account_age_timedelta.total_seconds() // 3600) % 24
        account_age_minutes = int(account_age_timedelta.total_seconds() // 60) % 60
        if account_age_days < 30:
            isNewUser = True
        if account_age_days >= 365:
            years = account_age_days // 365
            days_remaining = account_age_days % 365
            account_age = f"{years} years, {days_remaining} days."
        elif account_age_days > 1:
            account_age = f"{account_age_days} days, {account_age_hours} hours, {account_age_minutes} minutes."
        elif account_age_days == 1:
            account_age = (
                f"1 day, {account_age_hours} hours, {account_age_minutes} minutes."
            )
        elif account_age_hours > 0:
            account_age = f"{account_age_hours} hours, {account_age_minutes} minutes."
        else:
            account_age = f"{account_age_minutes} minutes."

        # Embed for the general channel
        title = "Member Joined"
        description = f"Welcome {member.mention} to the server!\nPlease familiarize yourself with the rules and enjoy your stay!"
        joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M")

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Joined at: {joined_at}")

        # Embed for the member details log
        detailEmbed = discord.Embed(
            title="Member Details",
            description=f"New User {member.mention} has joined the server.",
            color=discord.Color.red() if isNewUser else discord.Color.green(),
        )
        detailEmbed.add_field(
            name="Account Created",
            value=account_creation.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        detailEmbed.add_field(name="Account Age", value=account_age, inline=False)
        detailEmbed.add_field(name="Member Joined", value=joined_at, inline=False)

        (
            detailEmbed.add_field(name="New User", value="Yes", inline=False)
            if isNewUser
            else None
        )

        # Send the embeds to the appropriate channels
        await join_leave_channel.send(embed=embed)
        await member_details_channel.send(embed=detailEmbed)

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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            log_channel = self.bot.get_channel(
                config["configuration"]["reaction-log-channel"]
            )
            if log_channel is None:
                print("Reaction log channel not found.")
                return

            message = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            required_message_id = 1281471405887721545  # will get the message id from mySQL database later on
            await log_channel.send(
                f"Reaction {payload.emoji} added to message {message.jump_url}"
            )

            if payload.message_id == required_message_id:
                await log_channel.send(
                    f"Reaction added to specific message {message.jump_url}"
                )

        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Logger(bot))
