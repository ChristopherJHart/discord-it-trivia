"""Contains events relevant to joining guilds and utility functions."""

import structlog
from disnake import Guild
from bot.client import discord_bot


logger = structlog.get_logger(name=__name__)

__all__ = ["on_guild_join"]


@discord_bot.event
async def on_guild_join(guild: Guild) -> None:
    """Logs when bot joins a new guild."""
    logger.info("Joined guild", guild_id=guild.id, guild_name=guild.name)
