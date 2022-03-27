"""Kickstart bot and connect to Discord."""

# Initialize configuration management

from bot.core.config import settings

# Initialize logging

import logging
import sys
import structlog

from structlog.contextvars import merge_contextvars
from structlog.stdlib import filter_by_level

if settings.DEBUG:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

structlog.configure(
    logger_factory=structlog.stdlib.LoggerFactory(),
    context_class=structlog.threadlocal.wrap_dict(dict),
    processors=[
        filter_by_level,
        merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.getLogger(name=__name__)
logger.info("Logging initialized!")
logger.info("Disabling websockets debug logging")
logging.getLogger("websockets").setLevel(logging.INFO)
logging.getLogger("disnake.client").setLevel(logging.INFO)
logging.getLogger("disnake.gateway").setLevel(logging.INFO)

# Import events, commands, etc. so that they're properly registered by bot.

from bot.client import discord_bot  # noqa: E402
from bot.commands import *  # noqa: E402, F401, F403
from bot.events import *  # noqa: E402, F401, F403

# Create dynamic slash commands based on question pool

from disnake.ext import commands  # noqa: E402
from bot.commands.trivia import trivia  # noqa: E402
from bot.core.util import question_pool  # noqa: E402

pool = question_pool(settings.QUESTION_POOL_FILEPATH)

for exam in pool:
    command = commands.InvokableSlashCommand(
        trivia,
        name=exam.get("command_name"),
        description=exam.get("command_description"),
    )
    discord_bot.add_slash_command(command)
    logger.info(
        "Registered slash command",
        command_name=exam.get("command_name"),
        command_description=exam.get("command_description"),
    )

logger.info("Total text commands registered", total_commands=len(discord_bot.commands))
for command in discord_bot.commands:
    logger.info("Registered text command", command_name=command.name)

logger.info(
    "Total slash commands registered", total_commands=len(discord_bot.slash_commands)
)
for command in discord_bot.slash_commands:
    logger.info("Registered slash command", command_name=command.name)

# Connect to Discord

logger.info("Connecting to Discord")
discord_bot.run(settings.DISCORD_TOKEN)
logger.info("Connected to Discord!")
