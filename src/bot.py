import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.command(name='ping')
async def ping(ctx):
    """Simple command to check if the bot is responsive"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

# Run the bot
if __name__ == '__main__':
    print("Starting bot...")
    print(os.getenv('DISCORD_TOKEN'))
    token = os.getenv('DISCORD_TOKEN')
    print(token)
    if not token:
        raise ValueError("No token found! Make sure to set DISCORD_TOKEN in your .env file")
    bot.run(token) 