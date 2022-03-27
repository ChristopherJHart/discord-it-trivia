"""Contains events relevant to shard resuming."""

import structlog
from bot.client import discord_bot


logger = structlog.get_logger(name=__name__)

__all__ = ["on_shard_resumed"]


@discord_bot.event
async def on_shard_resumed(shard_id: int) -> None:
    """Triggers when a shard resumes."""
    logger.info(
        "Shard resumed",
        bot_name=discord_bot.user.name,
        bot_id=discord_bot.user.id,
        shard_id=shard_id,
    )
