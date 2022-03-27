"""Contains events relevant to general bot errors."""

import sys
import traceback
import hashlib
import structlog
from structlog.contextvars import clear_contextvars
from bot.client import discord_bot


logger = structlog.get_logger(name=__name__)

__all__ = ["on_error"]


@discord_bot.event
async def on_error(event, *args, **kwargs) -> None:
    """Handle any errors raised during async event hooks."""
    error = sys.exc_info()
    formatted_traceback = "".join(
        traceback.format_exception(error[0], error[1], error[2], 4)
    ).encode("utf-8")
    traceback_checksum = hashlib.sha1(formatted_traceback).hexdigest()
    logger.error(
        "Exception raised",
        error=error,
        traceback=formatted_traceback,
        checksum=traceback_checksum,
    )
    clear_contextvars()
