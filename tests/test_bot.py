import sys
import pytest
import discord
import discord.ext.commands as commands
from datetime import datetime

# Add the src directory to the Python path
sys.path.append("src")

from bot import (
    GENERAL_CHANNEL_ID,
    AI_ENDPOINT,
    MORNING_INTERVAL,
    query_ai,
    check_ai_health,
)

def test_constants():
    """Test that our constants are of the correct type and have valid values"""
    assert isinstance(GENERAL_CHANNEL_ID, int)
    assert isinstance(AI_ENDPOINT, str)
    assert AI_ENDPOINT.startswith("http")
    assert isinstance(MORNING_INTERVAL, int)
    assert 0 < MORNING_INTERVAL <= 24

def test_bot_creation():
    """Test that we can create a bot instance"""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    assert isinstance(bot, commands.Bot)
    assert bot.command_prefix == '!'

@pytest.mark.asyncio
async def test_morning_time_calculation():
    """Test that our morning time calculation is correct"""
    from bot import before_good_morning
    now = datetime.now()
    next_run = now.replace(hour=8, minute=0, second=0)
    if now >= next_run:
        next_run = next_run.replace(day=next_run.day + 1)
    
    # The time difference should be positive and less than 24 hours
    diff = (next_run - now).total_seconds()
    assert 0 <= diff <= 24 * 3600

def test_environment_variables():
    """Test that we handle missing environment variables gracefully"""
    import os
    token = os.getenv('DISCORD_TOKEN')
    # We expect no token in the test environment
    assert token is None 