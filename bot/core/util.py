"""Houses utility functions that don't fit elsewhere in the codebase."""

from typing import List, Optional
from yaml import SafeLoader, load
from aiohttp.client_exceptions import ClientOSError
from disnake import (
    ApplicationCommandInteraction,
    Embed,
    Forbidden,
    HTTPException,
    InteractionResponded,
)
from disnake.ui import View
from disnake.utils import MISSING
import structlog
from structlog.contextvars import (
    bind_contextvars,
    unbind_contextvars,
)

logger = structlog.getLogger(name=__name__)


def get_empty_embed_field_index(embed: Embed) -> Optional[int]:
    """Return the index of a field in an embed that is empty."""
    for index, field in enumerate(embed.fields):
        if not field.value.strip() or field.value is None:
            logger.warning(
                "Empty embed field",
                field_name=field.name,
                field_value=field.value,
                field_index=index,
            )
            return index
    return None


def remove_empty_embed_fields(embed: Embed) -> Embed:
    """Remove any empty fields present in an embed."""
    while index := get_empty_embed_field_index(embed):
        embed.remove_field(index)
    return embed


def normalize_embed(embed: Embed) -> List[Embed]:
    """Normalize one large embed by breaking it up into smaller embeds.

    Conform with Discord's embed limitations.
    """
    embeds = []
    # Normalize fields within the embed to ensure the embed abides by field limitations
    for index, field in enumerate(embed.fields):
        if len(field.value) > 1024:
            # Handle multi-line value elegantly
            lines = field.value.splitlines()
            if len(lines) > 1:  # Multiple lines present
                # Keep track of what lines in the field's value we're removing
                removed_lines = []
                for line_index in reversed(range(len(lines))):
                    modified_field_value = "\n".join(lines[:line_index])
                    if len(modified_field_value) <= 1024:
                        removed_lines.insert(0, lines[line_index])
                        embed.set_field_at(
                            index=index,
                            name=field.name,
                            value=modified_field_value,
                            inline=field.inline,
                        )
                        embed.insert_field_at(
                            index=index + 1,
                            name=field.name,
                            value="\n".join(removed_lines),
                            inline=field.inline,
                        )
                        break
            else:
                # Handle single-line value elegantly
                embed.set_field_at(
                    index=index,
                    name=field.name,
                    value=f"{field.value[:1021]}...",
                    inline=field.inline,
                )
                embed.insert_field_at(
                    index=index + 1,
                    name=field.name,
                    value=f"...{field.value[1021:]}",
                    inline=field.inline,
                )
    # Split up single large embed into multiple small embeds, if necessary
    embeds.append(embed)
    for e in embeds:
        if len(e) > 6000:
            # Copy the original embed so that we're not manipulating the original, which Python
            # doesn't like.
            new_embed = Embed(title=e.title, description=e.description, colour=e.color)
            # Iterate through the original embed (not the copy) from bottom to top.
            for index, field in reversed(list(enumerate(e.fields))):
                # "Migrate" the field from the original embed to the new embed. Then, delete the
                # field from the original embed copy.
                new_embed.insert_field_at(
                    index=0, name=field.name, value=field.value, inline=field.inline
                )
                e.remove_field(index)
                # Check to see if the copy (which has the field removed) is within Discord's embed
                # limitations. If so, add the new embed to our list of embeds and stop the loop
                # through the original embed's fields.
                if len(e) <= 6000:
                    embeds.append(new_embed)
                    break
    return embeds


def sanitize_embed(embed: Embed) -> List[Embed]:
    """Validate embed to make sure it's valid and normalized prior to sending."""
    embed = remove_empty_embed_fields(embed)
    return normalize_embed(embed)


async def send_embed(
    inter: ApplicationCommandInteraction,
    embed: Embed,
    ephemeral: bool = False,
    view: View = MISSING,
) -> None:
    """Send one or more embeds in response to a slash command."""
    embeds = sanitize_embed(embed)
    for e in embeds:
        bind_contextvars(
            guild_id=inter.guild.id,
            guild_name=inter.guild.name,
            channel_id=inter.channel.id,
            channel_name=inter.channel.name,
        )
        try:
            await inter.response.send_message(embed=e, ephemeral=ephemeral, view=view)
            logger.info("Sent embed", embed=e.to_dict())
        except InteractionResponded:
            await inter.followup.send(embed=e, ephemeral=ephemeral, view=view)
            logger.info("Sent embed", embed=e.to_dict())
        except Forbidden:
            logger.warning("Failed to send message due to permissions error")
        except HTTPException as exc:
            if exc.code == 50035:
                logger.warning(
                    "Invalid form body",
                    embed=e.to_dict(),
                )
        except ClientOSError:
            logger.warning(
                "Failed to send message due to client error",
            )
        finally:
            unbind_contextvars("guild_id", "guild_name", "channel_id", "channel_name")


def question_pool(filepath: str) -> List[dict]:
    """Open question pool YAML file and return contents."""
    with open(filepath) as pool_file:
        return load(pool_file, SafeLoader)


def exam_from_pool(exam_name: str) -> Optional[List[dict]]:
    """Get data about exam from question pool."""
    # TODO: Import here so unit tests work properly. This is a hack, refactor later.
    from bot.core.config import settings

    pool = question_pool(settings.QUESTION_POOL_FILEPATH)
    for exam in pool:
        if exam.get("command_name") == exam_name:
            return exam
