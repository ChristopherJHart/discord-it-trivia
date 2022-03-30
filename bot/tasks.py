"""Contains scheduled tasks executed by bot."""

import structlog
from disnake.ext import tasks
from bot.client import discord_bot

logger = structlog.getLogger(name=__name__)


@tasks.loop(hours=1)
async def log_guild_quantity() -> None:
    """Log the quantity of guilds bot is joined to."""
    await discord_bot.wait_until_ready()
    logger.info("Guild information", number_of_guilds=len(discord_bot.guilds))
