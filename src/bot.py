import os
import sys
import discord
import aiohttp
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Configure logging to stdout
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Constants
GENERAL_CHANNEL_ID = 670339732059979807
AI_ENDPOINT = "http://192.168.0.192:5000/v1/completions"
MORNING_INTERVAL = 23  # hours

# Load environment variables
load_dotenv()
logger.info("Starting bot initialization...")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def query_ai(prompt):
    """Query the AI endpoint with a prompt"""
    try:
        payload = {
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.6,
            "seed": 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(AI_ENDPOINT, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('text', 'No response from AI')
                else:
                    logger.error(f"AI API error: {response.status}")
                    return "Sorry, I couldn't get a response from the AI right now."
    except Exception as e:
        logger.error(f"Error querying AI: {e}")
        return "Sorry, there was an error communicating with the AI."

async def check_ai_health():
    """Check if the AI endpoint is responsive"""
    try:
        response = await query_ai("Return OK if you're working.")
        if response and len(response.strip()) > 0:
            logger.info("AI endpoint health check passed")
            return True
        else:
            logger.error("AI endpoint health check failed: Got empty response")
            return False
    except Exception as e:
        logger.error(f"AI endpoint health check failed: {e}")
        return False

@tasks.loop(hours=MORNING_INTERVAL)
async def send_good_morning():
    """Send good morning message every 23 hours"""
    channel = bot.get_channel(GENERAL_CHANNEL_ID)
    if channel:
        await channel.send("Good moring! 🌅")
        logger.info("Sent good morning message")
    else:
        logger.error("Could not find general channel")

@send_good_morning.before_loop
async def before_good_morning():
    """Wait until the bot is ready before starting the good morning loop"""
    await bot.wait_until_ready()
    # Wait until next 8 AM
    now = datetime.now()
    next_run = now.replace(hour=8, minute=0, second=0)
    if now >= next_run:
        next_run = next_run + timedelta(days=1)
    await asyncio.sleep((next_run - now).seconds)

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # Check AI endpoint health
    logger.info("Performing AI endpoint health check...")
    is_healthy = await check_ai_health()
    
    if is_healthy:
        # Start the good morning task only if AI is healthy
        send_good_morning.start()
        logger.info("Bot startup complete - AI endpoint is healthy")
    else:
        logger.warning("Bot started but AI endpoint is not responding - some features may not work")

on_message_hooks = []

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    for hook in on_message_hooks:
        try:
            await hook(message)
        except Exception as e:
            logger.error(f"Error in message hook: {e}")

def register_hook(hook):
    try:
        on_message_hooks.append(hook)
    except:
        logger.error("Failed to register hook")



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