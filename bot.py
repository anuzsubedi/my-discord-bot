import asyncio
import discord
from discord.ext import commands
import yaml
import utils.dbmanager as db

# Load the configuration from the YAML file
def load_config(path="./config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

# Initialize database manager and run migrations
def init_db():
    db_manager = db.DatabaseManager()
    db_manager.check_migration()
    return db_manager

# Load bot intents and command prefix from config
def init_bot(config):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    intents.members = True

    bot = commands.Bot(command_prefix=config["discord"]["prefix"], intents=intents)

    # Event handlers need to be defined here after bot initialization
    @bot.event
    async def on_ready():
        synced_commands = await bot.tree.sync()  # Sync slash commands globally
        print(f"Synced {len(synced_commands)} commands globally.")
        print(f"Bot is online and logged in as {bot.user.name}")

    @bot.event
    async def on_connect():
        print(f"Connected to Discord!")
    
    return bot

# Load the cogs (command sets)
async def load_cogs(bot):
    cogs = [
        "cogs.moderator",
        "cogs.user",
        "cogs.logger",
        "cogs.admin",
        "cogs.configuration",
    ]
    for cog in cogs:
        await bot.load_extension(cog)

# Main function to start the bot
async def main():
    config = load_config()
    init_db()
    
    bot = init_bot(config)
    await load_cogs(bot)
    await bot.start(config["discord"]["token"])

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
