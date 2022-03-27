"""Houses the disnake client for bot accessed by commands and events."""

import structlog
from disnake.ext import commands
from disnake import AllowedMentions, Intents
from bot.core.config import settings

logger = structlog.getLogger(name=__name__)


logger.info("Instantiating bot")
intents = Intents.default()

sync_commands_debug = True if settings.TEST_GUILD else False

if sync_commands_debug and settings.TEST_GUILD is not None:
    discord_bot = commands.AutoShardedBot(
        allowed_mentions=AllowedMentions(everyone=False),
        max_messages=10000,
        help_command=None,
        test_guilds=[settings.TEST_GUILD],
        sync_commands_debug=sync_commands_debug,
    )
else:
    discord_bot = commands.AutoShardedBot(
        allowed_mentions=AllowedMentions(everyone=False),
        intents=intents,
        max_messages=10000,
        help_command=None,
    )

logger.info("Bot instantiated")
