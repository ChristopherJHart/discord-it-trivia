"""Contains events relevant to when bot is ready to work."""

import structlog
from bot.client import discord_bot
from bot.tasks import log_guild_quantity


logger = structlog.get_logger(name=__name__)

__all__ = ["on_ready"]


@discord_bot.event
async def on_ready():
    """Triggers when the bot is fully connected and ready to do work."""
    logger.info("Logged in", bot_name=discord_bot.user.name, bot_id=discord_bot.user.id)
    tasks = [log_guild_quantity]
    for task in tasks:
        if not task.is_running():
            task.start()
