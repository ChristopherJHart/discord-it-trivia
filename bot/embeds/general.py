"""Contains general command-related embeds and decorators."""

from functools import wraps
from disnake import Embed, Colour
from disnake.utils import utcnow
from bot.models.icon_urls import OK_ICON, WRONG_ICON, CRITICAL_ICON

__all__ = [
    "command_embed",
    "command_ok",
    "command_wrong",
    "command_error",
    "command_failed",
]


def command_embed(title: str, icon: str, colour: Colour) -> Embed:
    """Base embed for all command embeds."""
    embed = Embed(title=title, timestamp=utcnow(), colour=colour)
    embed.set_thumbnail(url=icon)
    return embed


def command_ok(title: str = "__Command Successful__") -> Embed:
    """Base embed for all OK command embeds."""

    def decorator_ok(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            emb = command_embed(title=title, icon=OK_ICON, colour=Colour.green())
            func(emb, *args, **kwargs)
            return emb

        return wrapper

    return decorator_ok


def command_wrong(title: str = "__Command Unsuccessful__") -> Embed:
    """Base embed for command embeds indicating something is wrong."""

    def decorator_ok(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            emb = command_embed(title=title, icon=WRONG_ICON, colour=Colour.red())
            func(emb, *args, **kwargs)
            return emb

        return wrapper

    return decorator_ok


def command_error():
    """Base embed for all slash command error embeds."""

    def decorator_error(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            embed = command_embed(
                title="__Command Error__", icon=CRITICAL_ICON, colour=Colour.red()
            )

            func(embed, *args, **kwargs)
            return embed

        return wrapper

    return decorator_error


@command_error()
def command_failed(
    embed: Embed, command: str, error_checksum: str, error_id: str, traceback: str
) -> Embed:
    """Embed for slash commands that fail."""
    # embed.add_field(
    #     name="Error",
    #     value=(
    #         "Please contact support through the `!support` command and provide the below "
    #         "information."
    #     ),
    #     inline=False,
    # )
    embed.add_field(name="Failed Command", value=f"`/{command}`", inline=False)
    embed.add_field(name="Generic Error ID", value=error_checksum, inline=False)
    embed.add_field(name="Unique Error ID", value=error_id, inline=False)
    embed.add_field(name="Traceback", value=f"```\n{traceback}\n```", inline=False)
    return embed
