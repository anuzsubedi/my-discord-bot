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


async def setup(bot):
    await bot.add_cog(Logger(bot))
