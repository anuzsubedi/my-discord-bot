import datetime
import discord
from discord.ext import commands
import pytz
from utils.dbmanager import DatabaseManager


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Triggered when the bot joins a new guild."""
        try:
            self.db_manager.insert_server(guild.id)
        except Exception as e:
            print(f"An error occurred while inserting server: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Triggered when a new member joins the guild."""
        try:
            join_leave_channel, member_details_channel = await self.get_channels(member.guild.id)

            # Log the channel retrieval for debugging
            if not join_leave_channel:
                print(f"Join-Leave channel not found for guild: {member.guild.id}")
            if not member_details_channel:
                print(f"Member details channel not found for guild: {member.guild.id}")

            account_age, is_new_user = self.calculate_account_age(member)

            # Send the welcome message if the join_leave_channel exists
            if join_leave_channel:
                await self.send_welcome_message(member, join_leave_channel, account_age)
                print(f"Welcome message sent to {member.name} in {join_leave_channel.id}.")
            else:
                print(f"Join-Leave channel missing, welcome message not sent for {member.name}.")

            # Log the member details if the member_details_channel exists
            if member_details_channel:
                await self.log_member_details(member, member_details_channel, account_age, is_new_user)
                print(f"Member details log sent for {member.name} in {member_details_channel.id}.")
            else:
                print(f"Member details log not sent for {member.name}: Channel missing.")
                
        except Exception as e:
            print(f"An error occurred while processing member join: {e}")

    async def get_channels(self, guild_id):
        """Retrieve the join-leave and member details channels from the database."""
        try:
            join_leave_channel_id = self.db_manager.get_join_leave_channel(guild_id)
            member_details_channel_id = self.db_manager.get_member_detail_channel(guild_id)

            join_leave_channel = self.bot.get_channel(join_leave_channel_id) if join_leave_channel_id else None
            member_details_channel = self.bot.get_channel(member_details_channel_id) if member_details_channel_id else None

            # Log channel retrieval for debugging
            print(f"Join-Leave Channel ID: {join_leave_channel_id}, Member Details Channel ID: {member_details_channel_id}")
            
            return join_leave_channel, member_details_channel
        except Exception as e:
            print(f"An error occurred while retrieving channels: {e}")
            return None, None

    def calculate_account_age(self, member):
        """Calculate account age and check if the user is new."""
        account_creation = member.created_at.astimezone(pytz.UTC)
        now = datetime.datetime.now(pytz.UTC)
        account_age_days = (now - account_creation).days
        is_new_user = account_age_days < 30

        if account_age_days >= 365:
            years = account_age_days // 365
            days_remaining = account_age_days % 365
            account_age = f"{years} years, {days_remaining} days."
        elif account_age_days > 1:
            account_age = f"{account_age_days} days."
        elif account_age_days == 1:
            account_age = "1 day."
        else:
            account_age = f"{(now - account_creation).seconds // 3600} hours."

        return account_age, is_new_user

    async def send_welcome_message(self, member, join_leave_channel, account_age):
        """Send a welcome message to the join/leave channel."""
        embed = discord.Embed(
            title="Member Joined",
            description=f"Welcome {member.mention} to the server! Please familiarize yourself with the rules and enjoy your stay!",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Joined at: {member.joined_at.strftime('%Y-%m-%d %H:%M')}")
        await join_leave_channel.send(embed=embed)

    async def log_member_details(self, member, member_details_channel, account_age, is_new_user):
        """Log the member's details in the member details channel."""
        detail_embed = discord.Embed(
            title="Member Details",
            description=f"New User {member.mention} has joined the server.",
            color=discord.Color.red() if is_new_user else discord.Color.green(),
        )
        detail_embed.add_field(
            name="Account Created",
            value=member.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        detail_embed.add_field(name="Account Age", value=account_age, inline=False)
        if is_new_user:
            detail_embed.add_field(name="New User", value="Yes", inline=False)

        await member_details_channel.send(embed=detail_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Triggered when a member leaves the guild."""
        try:
            join_leave_channel, _ = await self.get_channels(member.guild.id)
            if not join_leave_channel or not member.joined_at:
                return

            left_after = self.calculate_time_spent(member)
            embed = discord.Embed(
                title="Member Left",
                description=f"Goodbye {member.mention}!\nWe hope to see you again soon!",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"{member.name} was here for {left_after}")
            await join_leave_channel.send(embed=embed)
        except Exception as e:
            print(f"An error occurred while processing member removal: {e}")

    def calculate_time_spent(self, member):
        """Calculate the time a member spent on the server."""
        now = datetime.datetime.now(pytz.UTC)
        difference = now - member.joined_at.astimezone(pytz.UTC)
        days = difference.days
        hours, remainder = divmod(difference.seconds, 3600)
        minutes = remainder // 60
        return f"{days} days, {hours} hours, {minutes} minutes."


async def setup(bot):
    await bot.add_cog(Logger(bot))
