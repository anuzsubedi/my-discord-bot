import datetime
import discord
from discord.ext import commands
import yaml
import pytz
from utils.dbmanager import DatabaseManager


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()  # Instantiate DatabaseManager
        self.config = self.load_config()

    def load_config(self, config_path="./config.yaml"):
        """Load bot configuration from YAML file."""
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file {config_path} not found.")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return None

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
            join_leave_channel, member_details_channel = self.get_channels()

            if not join_leave_channel or not member_details_channel:
                return

            account_age, is_new_user = self.calculate_account_age(member)
            await self.send_welcome_message(member, join_leave_channel, account_age)
            await self.log_member_details(member, member_details_channel, account_age, is_new_user)
        except Exception as e:
            print(f"An error occurred while processing member join: {e}")

    def get_channels(self):
        """Retrieve the channels for join/leave and member details."""
        return (
            self.bot.get_channel(self.config["configuration"]["join-leave-channel"]),
            self.bot.get_channel(self.config["configuration"]["member-detail-log-channel"]),
        )

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
            join_leave_channel = self.bot.get_channel(self.config["configuration"]["join-leave-channel"])
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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_reaction(payload, added=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_reaction(payload, added=False)

    async def handle_reaction(self, payload, added):
        """Handle reactions being added or removed."""
        try:
            required_message_id = 1281471405887721545  # Placeholder for message ID
            role_id = 1281476972966576202  # Placeholder for role ID
            log_channel = self.bot.get_channel(self.config["configuration"]["reaction-log-channel"])

            if log_channel is None:
                print("Reaction log channel not found.")
                return

            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            member = message.guild.get_member(payload.user_id)

            if member is None or payload.message_id != required_message_id:
                return

            action = "added" if added else "removed"
            await log_channel.send(f"Reaction {action} to specific message {message.jump_url}")

            role = message.guild.get_role(role_id)
            if added:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

        except Exception as e:
            print(f"An error occurred while handling reaction: {e}")


async def setup(bot):
    await bot.add_cog(Logger(bot))
