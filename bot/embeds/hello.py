"""/hello user feedback embeds."""

from disnake import Embed
from bot import __version__
from .general import (
    command_ok,
)

__all__ = ["hello_ok_reply"]


@command_ok(title="__Hello!__")
def hello_ok_reply(embed: Embed, latency: float) -> Embed:
    """Embed for valid `!hello` command reply.

    Args:
        embed (Embed): Embed to modify.
        latency (float): Discord API latency measured in seconds.
    """
    embed.add_field(name="Version", value=f"v{__version__}", inline=False)
    embed.add_field(
        name="Discord API Latency", value=f"{(latency * 1000):.2f} ms", inline=False
    )
    return embed
