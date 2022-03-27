"""Contains events relevant to command errors."""

import traceback
from uuid import uuid4
import hashlib
import structlog
from structlog.contextvars import clear_contextvars, bind_contextvars
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from bot.client import discord_bot
from bot.core.util import send_embed
from bot.embeds import command_failed


logger = structlog.get_logger(name=__name__)

__all__ = ["on_slash_command_error"]


@discord_bot.event
async def on_slash_command_error(
    inter: ApplicationCommandInteraction, error: commands.CommandError
) -> None:
    """Handle any errors raised during async command-driven events.

    The current implementation logs any exceptions that arise as a result
    of a command as a warning. Ideally, all possible exceptions that can be
    raised as a result of a command should be gracefully handled by the bot,
    so this *should* never happen. If this event is triggered, an enhancement
    should be filed to prevent it from happening again in the future.
    """
    clear_contextvars()
    bind_contextvars(
        guild_id=inter.guild.id,
        guild_name=inter.guild.name,
        user_id=inter.author.id,
        user_name=inter.author.name,
        channel_id=inter.channel.id,
        channel_name=inter.channel.name,
        command=inter.data.name,
    )
    unique_error_id = str(uuid4())
    formatted_traceback = "".join(
        traceback.format_exception(type(error), error, error.__traceback__, 4)
    ).encode("utf-8")
    traceback_checksum = hashlib.sha1(formatted_traceback).hexdigest()
    logger.warning(
        "Command failed",
        error=error,
        traceback="".join(
            traceback.format_exception(type(error), error, error.__traceback__, 4)
        ),
        checksum=traceback_checksum,
        error_id=unique_error_id,
    )
    await send_embed(
        inter,
        command_failed(
            command=inter.data.name,
            error_checksum=traceback_checksum,
            error_id=unique_error_id,
            traceback=formatted_traceback,
        ),
    )
    clear_contextvars()
