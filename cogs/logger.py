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
    async def on_ready(self):
        print("Logger cog is ready.")
        log_channel = self.bot.get_channel(
            config["configuration"]["public-log-channel"]
        )
        await log_channel.send("Logger cog is ready.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        log_channel = self.bot.get_channel(
            config["configuration"]["public-log-channel"]
        )
        await log_channel.send(
            f"Message from {message.author} in {message.channel}: {message.content}"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(
            config["configuration"]["public-log-channel"]
        )
        await log_channel.send("Someone has joined the server.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        log_channel = self.bot.get_channel(
            config["configuration"]["public-log-channel"]
        )
        await log_channel.send(
            f"Message from {message.author} in {message.channel}: {message.content}"
        )


async def setup(bot):
    await bot.add_cog(Logger(bot))
