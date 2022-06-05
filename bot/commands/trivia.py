"""Contains coroutines for dynamically-created trivia commands."""

from random import choice, shuffle
import structlog
from structlog.contextvars import clear_contextvars, bind_contextvars
from disnake import ApplicationCommandInteraction
from bot.views import AnswerChoices
from bot.embeds.trivia import (
    trivia_ok_multiple_choice_question,
)
from bot.core.util import send_embed, exam_from_pool

logger = structlog.getLogger(name=__name__)


async def trivia(inter: ApplicationCommandInteraction) -> None:
    """Asks a trivia question based upon the invoker command.

    This coroutine is passed into a dynamically-created slash command. Each exam in the question
    pool gets its own command.
    """
    clear_contextvars()
    bind_contextvars(
        guild_id=inter.guild.id,
        guild_name=inter.guild.name,
        channel_id=inter.channel.id,
        channel_name=inter.channel.name,
        command_name=inter.application_command.name,
    )
    exam = exam_from_pool(inter.application_command.name)
    question = choice(exam.get("questions"))
    prompt = question.get("prompt")
    answer_choices = question.get("choices")
    shuffle(answer_choices)
    answer_choice_view = AnswerChoices(
        choices=answer_choices,
        correct_choice_id=question.get("correct_choice"),
        explanation=question.get("explanation"),
    )
    await send_embed(
        inter,
        trivia_ok_multiple_choice_question(
            exam.get("meta_name"), prompt, [c.get("text") for c in answer_choices]
        ),
        view=answer_choice_view,
    )
    clear_contextvars()
