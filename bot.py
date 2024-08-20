import asyncio
import discord
from discord.ext import commands
import yaml

# Load the configuration from the YAML file
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Access specific settings
DISCORD_TOKEN = config["discord"]["token"]
PREFIX = config["discord"]["prefix"]

# Initialize the bot with intents and command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# Load the cogs (command sets)
async def load_cogs():
    cogs = ["cogs.moderator", "cogs.user", "cogs.logger", "cogs.admin"]
    for cog in cogs:
        await bot.load_extension(cog)


# Sync the slash commands with Discord and show the count
@bot.event
async def on_ready():
    synced_commands = await bot.tree.sync()  # Sync slash commands globally
    print(f"Synced {len(synced_commands)} commands globally.")
    print(f"Bot is online and logged in as {bot.user.name}")


@bot.event
async def on_connect():
    print(f"Connected to Discord!")


# Start the bot using the token from the config
async def main():
    await load_cogs()
    await bot.start(DISCORD_TOKEN)


asyncio.run(main())
