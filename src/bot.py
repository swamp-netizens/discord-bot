import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging to stdout
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Starting bot initialization...")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_message(message):
    # Don't respond to our own messages
    if message.author == bot.user:
        return

    # Log message details
    logger.info(f'Message from {message.author} in #{message.channel}: "{message.content}"')
    
    # Don't forget this line if you want commands to work too!
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    """Simple command to check if the bot is responsive"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

# Run the bot
if __name__ == '__main__':
    logger.info("Starting bot...")
    token = os.getenv('DISCORD_TOKEN')
    
    # Debug token presence (don't log the actual token!)
    if token:
        logger.info("Discord token found")
        masked_token = token[:6] + '...' + token[-4:]
        logger.info(f"Token starts with: {masked_token}")
    else:
        logger.error("No Discord token found in environment!")
        sys.exit(1)

    logger.info("Attempting to start bot with token...")
    bot.run(token) 