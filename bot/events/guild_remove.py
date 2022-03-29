"""Contains events relevant to leaving guilds and utility functions."""

import structlog
from disnake import Guild
from bot.client import discord_bot


logger = structlog.get_logger(name=__name__)

__all__ = ["on_guild_remove"]


@discord_bot.event
async def on_guild_remove(guild: Guild) -> None:
    """Logs when bot is removed from a guild."""
    logger.info("Removed from guild", guild_id=guild.id, guild_name=guild.name)
