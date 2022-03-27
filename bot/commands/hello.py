"""Contains slash command for /hello."""

from disnake import ApplicationCommandInteraction
from bot.client import discord_bot
from bot.embeds import hello_ok_reply
from bot.core.util import send_embed


__all__ = ["hello"]


@discord_bot.slash_command()
async def hello(
    inter: ApplicationCommandInteraction,
) -> None:
    """Simple ping/pong hello command."""
    await send_embed(inter, hello_ok_reply(discord_bot.latency))
