"""Contains coroutines for dynamically-created trivia commands."""

from random import choice, shuffle
import asyncio
from datetime import datetime, timedelta
import structlog
from disnake import ApplicationCommandInteraction, Reaction, Member
from bot.client import discord_bot
from bot.embeds.trivia import (
    trivia_ok_multiple_choice_question,
    trivia_ok_correct,
    trivia_ok_incorrect,
)
from bot.core.config import settings
from bot.core.util import send_embed, exam_from_pool

logger = structlog.getLogger(name=__name__)


async def trivia(inter: ApplicationCommandInteraction) -> None:
    """Asks a trivia question based upon the invoker command.

    This coroutine is passed into a dynamically-created slash command. Each exam in the question
    pool gets its own command.
    """
    exam = exam_from_pool(inter.application_command.name)
    question = choice(exam.get("questions"))
    prompt = question.get("prompt")
    answer_choices = question.get("choices")
    shuffle(answer_choices)
    await send_embed(
        inter,
        trivia_ok_multiple_choice_question(
            exam.get("meta_name"), prompt, [c.get("text") for c in answer_choices]
        ),
    )

    # Add reactions
    response = await inter.original_message()
    index_to_emoji_mapping = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }
    for index, answer_choice in enumerate(answer_choices, start=1):
        await response.add_reaction(index_to_emoji_mapping.get(index))

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=settings.QUESTION_TIMEOUT)
    logger.info(
        "New question active",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
    )
    while datetime.now() < end_time:

        def check(reaction: Reaction, member: Member) -> bool:
            return (
                reaction.message.id == response.id and member.id != discord_bot.user.id
            )

        try:
            logger.info("Waiting for next reaction")
            reaction, user = await discord_bot.wait_for(
                "reaction_add", timeout=settings.QUESTION_TIMEOUT, check=check
            )
        except asyncio.TimeoutError:
            pass
        else:
            logger.info("Received reaction", reaction=reaction)
            selected_index = None
            selected_answer_choice = None
            for index, emoji in index_to_emoji_mapping.items():
                if str(reaction.emoji) == emoji:
                    selected_index = index
            logger.info("Selected reaction index", selected_index=selected_index)
            if selected_index is not None:
                for index, answer_choice in enumerate(answer_choices, start=1):
                    if selected_index == index:
                        selected_answer_choice = answer_choice

            logger.info(
                "Select answer choice", selected_answer_choice=selected_answer_choice
            )
            if selected_answer_choice is not None:
                logger.info(
                    "Comparing selected answer choice with correct answer",
                    selected_answer_choice_id=selected_answer_choice.get("id"),
                    correct_answer_choice_id=question.get("correct_choice"),
                )
                if selected_answer_choice.get("id") == question.get("correct_choice"):
                    await inter.followup.send(embed=trivia_ok_correct(), ephemeral=True)
                else:
                    for index, answer_choice in enumerate(answer_choices, start=1):
                        if answer_choice.get("id") == question.get("correct_choice"):
                            await inter.followup.send(
                                embed=trivia_ok_incorrect(
                                    f"{index}. {answer_choice.get('text')}"
                                ),
                                ephemeral=True,
                            )

    logger.info("Question is no longer active")
