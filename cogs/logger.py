import datetime
import discord
from discord.ext import commands
import yaml
import pytz
from utils.dbmanager import DatabaseManager

# Load the configuration from the YAML file
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()  # Instantiate DatabaseManager

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            guild_id = guild.id
            self.db_manager.insert_server(guild_id)  #
        except Exception as e:
            print(f"An error occurred while inserting server: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        isNewUser = False
        join_leave_channel = self.bot.get_channel(
            config["configuration"]["join-leave-channel"]
        )
        member_details_channel = self.bot.get_channel(
            config["configuration"]["member-detail-log-channel"]
        )

        if join_leave_channel is None or member_details_channel is None:
            return

        account_creation = member.created_at.astimezone(pytz.UTC)
        now = datetime.datetime.now(pytz.UTC)
        account_age_timedelta = now - account_creation
        account_age_days = account_age_timedelta.days

        if account_age_days < 30:
            isNewUser = True

        # Calculate account age
        if account_age_days >= 365:
            years = account_age_days // 365
            days_remaining = account_age_days % 365
            account_age = f"{years} years, {days_remaining} days."
        elif account_age_days > 1:
            account_age = f"{account_age_days} days."
        elif account_age_days == 1:
            account_age = "1 day."
        else:
            account_age = f"{account_age_timedelta.seconds // 3600} hours."

        title = "Member Joined"
        description = f"Welcome {member.mention} to the server! Please familiarize yourself with the rules and enjoy your stay!"
        joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M")

        embed = discord.Embed(
            title=title, description=description, color=discord.Color.green()
        )
        embed.set_footer(text=f"Joined at: {joined_at}")

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
        if isNewUser:
            detailEmbed.add_field(name="New User", value="Yes", inline=False)

        await join_leave_channel.send(embed=embed)
        await member_details_channel.send(embed=detailEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        join_leave_channel = self.bot.get_channel(
            config["configuration"]["join-leave-channel"]
        )
        if join_leave_channel is None or member.joined_at is None:
            return

        try:
            joined_at = member.joined_at.astimezone(pytz.UTC)
            now = datetime.datetime.now(pytz.UTC)
            difference = now - joined_at
            days = difference.days
            hours, minutes = divmod(int(difference.total_seconds()), 3600)
            hours %= 24
            left_after = f"{days} days, {hours} hours, {minutes} minutes."

            embed = discord.Embed(
                title="Member Left",
                description=f"Goodbye {member.mention}!\nWe hope to see you again soon!",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"{member.name} was here for {left_after}")

            await join_leave_channel.send(embed=embed)
        except Exception as e:
            print(f"An error occurred while processing member removal: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_reaction(payload, added=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_reaction(payload, added=False)

    async def handle_reaction(self, payload, added):
        try:
            required_message_id = (
                1281471405887721545  # Placeholder for message ID from DB
            )
            role_id = 1281476972966576202  # Placeholder for role ID from DB
            log_channel = self.bot.get_channel(
                config["configuration"]["reaction-log-channel"]
            )
            if log_channel is None:
                print("Reaction log channel not found.")
                return

            message = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            member = message.guild.get_member(payload.user_id)
            if member is None:
                print("Member not found.")
                return

            if payload.message_id == required_message_id:
                action = "added" if added else "removed"
                await log_channel.send(
                    f"Reaction {action} to specific message {message.jump_url}"
                )
                role_action = member.add_roles if added else member.remove_roles
                await role_action(message.guild.get_role(role_id))

        except Exception as e:
            print(f"An error occurred while handling reaction: {e}")


async def setup(bot):
    await bot.add_cog(Logger(bot))
