"""Contains events relevant to completed commands."""

import structlog
from disnake import ApplicationCommandInteraction
from bot.client import discord_bot


logger = structlog.get_logger(name=__name__)

__all__ = ["on_slash_command_completion"]


@discord_bot.event
async def on_slash_command_completion(inter: ApplicationCommandInteraction) -> None:
    """Log that command was completed successfully."""
    logger.info(
        "Command completed",
        command_name=inter.data.name,
        message_author_id=inter.author.id,
        message_author_name=inter.author.name,
        guild_id=inter.guild.id,
        guild_name=inter.guild.name,
    )
