import discord
from discord.ext import commands
from discord import app_commands
import yaml

# Load the configuration from the YAML file
with open("./config.yaml", "r") as file:
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

    @app_commands.command(
        name="announce", description="Send an announcement to the announcement channel."
    )
    async def announce(self, ctx: discord.Interaction, message: str):
        try:
            message = message.replace("\\n", "\n")
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                announcement_channel = self.bot.get_channel(
                    config["configuration"]["announcement-channel"]
                )
                await announcement_channel.send(message)
                await ctx.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="embedannounce", description="Send an announcement as an embed."
    )
    async def embedannounce(
        self, ctx: discord.Interaction, title: str, description: str
    ):
        try:
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                announcement_channel = self.bot.get_channel(
                    config["configuration"]["announcement-channel"]
                )
                embed = discord.Embed(
                    title=title,
                    description=description.replace("\\n", "\n"),
                    color=discord.Color.green(),
                )
                await announcement_channel.send(embed=embed)
                await ctx.response.send_message(
                    f"Announcement sent to {announcement_channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="sendbotmessage",
        description="Send a message as the bot in specified channel.",
    )
    async def sendbotmessagae(
        self, ctx: discord.Interaction, channel: discord.TextChannel, message: str
    ):
        try:
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                await channel.send(message.replace("\\n", "\n"))
                await ctx.response.send_message(
                    f"Message sent to {channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="sendbotembed",
        description="Send an embed message as the bot in specified channel.",
    )
    async def send_bot_embed(
        self,
        ctx: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        description: str,
    ):
        try:
            if ctx.user.guild_permissions.administrator or self.check_mod(ctx):
                embed = discord.Embed(
                    title=title,
                    description=description.replace("\\n", "\n"),
                    color=discord.Color.green(),
                )
                await channel.send(embed=embed)
                await ctx.response.send_message(
                    f"Embed message sent to {channel.mention}.",
                    ephemeral=True,
                )
            else:
                await ctx.response.send_message(
                    "You are not allowed to use this command.", ephemeral=True
                )
        except Exception as e:
            print(f"\n++++++++++++\n")
            print(e)

    @app_commands.command(
        name="purgeall", description="Delete up to 1000 messages in the channel."
    )
    async def purge_all(self, interaction: discord.Interaction):
        # Check if the user has the 'Manage Messages' permission
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        try:
            # Acknowledge the interaction immediately
            await interaction.response.defer(ephemeral=True)

            # Purge up to 1000 messages in the channel
            deleted = await interaction.channel.purge(limit=1000)

            # Send a follow-up message with the result
            await interaction.followup.send(
                f"Successfully deleted {len(deleted)} messages.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "I do not have permission to delete messages in this channel.",
                ephemeral=True,
            )

    @app_commands.command(
        name="purge", description="Delete a specific number of messages in the channel."
    )
    async def purge(self, interaction: discord.Interaction, amount: int):
        # Check if the user has the 'Manage Messages' permission
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        try:
            # Acknowledge the interaction immediately
            await interaction.response.defer(ephemeral=True)

            # Purge the specified number of messages in the channel
            deleted = await interaction.channel.purge(limit=amount)

            # Send a follow-up message with the result
            await interaction.followup.send(
                f"Successfully deleted {len(deleted)} messages.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "I do not have permission to delete messages in this channel.",
                ephemeral=True,
            )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Moderator(bot))
