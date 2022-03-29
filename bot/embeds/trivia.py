"""Trivia command user feedback embeds."""

from typing import List, Optional
from disnake import Embed
from .general import (
    command_ok,
    command_wrong,
)

__all__ = [
    "trivia_ok_multiple_choice_question",
    "trivia_ok_correct",
    "trivia_ok_incorrect",
]


@command_ok()
def trivia_ok_multiple_choice_question(
    embed: Embed, exam_name: str, prompt: str, choices: List[str]
) -> Embed:
    """Embed for valid `!hello` command reply.

    Args:
        embed (Embed): Embed to modify.
        exam_name (str): Name of exam to insert into embed title.
        prompt (str): Question asked to users.
        choices (List[str]): Randomized list of possible answer choices.
    """
    embed.title = f"__{exam_name}__"
    embed.add_field(name="Question", value=prompt, inline=False)
    value = ["```"]
    for index, choice in enumerate(choices, start=1):
        value.append(f"{index}. {choice}")
    value.append("```")
    embed.add_field(name="Answer Choices", value="\n".join(value), inline=False)
    return embed


@command_ok(title="__Trivia Answer Correct__")
def trivia_ok_correct(embed: Embed, explanation: Optional[str] = None) -> Embed:
    """Embed for when answer to trivia question is correct."""
    embed.add_field(
        name="Response",
        value="Your answer to the trivia question was correct!",
        inline=False,
    )
    if explanation is not None:
        embed.add_field(name="Explanation", value=explanation, inline=False)
    return embed


@command_wrong(title="__Trivia Answer Incorrect__")
def trivia_ok_incorrect(
    embed: Embed, correct_answer: str, explanation: Optional[str] = None
) -> Embed:
    """Embed for when answer to trivia question is incorrect."""
    embed.add_field(
        name="Response",
        value="Your answer to the trivia question was incorrect.",
        inline=False,
    )
    embed.add_field(name="Correct Answer", value=correct_answer, inline=False)
    if explanation is not None:
        embed.add_field(name="Explanation", value=explanation, inline=False)
    return embed
