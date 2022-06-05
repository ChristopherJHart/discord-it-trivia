"""Contains views relevant to trivia questions."""

from typing import List, Optional
import structlog
import disnake
from bot.embeds.trivia import trivia_ok_correct, trivia_ok_incorrect

logger = structlog.getLogger(name=__name__)


class AnswerChoice(disnake.ui.Button):
    """Button representing an answer choice for a question."""

    def __init__(
        self,
        correct: bool,
        correct_choice_text: str,
        choice_id: int,
        explanation: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        """Instantiate a new answer choice."""
        self.correct: bool = correct
        self.correct_choice_text: str = correct_choice_text
        self.choice_id: int = choice_id
        self.explanation: str = explanation

        super().__init__(*args, **kwargs)

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        """Inform user whether their choice is correct or incorrect."""
        logger.info(
            "Answer selected",
            choice_id=self.choice_id,
            choice_text=self.label,
            choice_correct=self.correct,
            guild_id=interaction.guild_id,
            guild_name=interaction.guild.name,
        )
        if self.correct:
            await interaction.response.send_message(
                embed=trivia_ok_correct(explanation=self.explanation),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=trivia_ok_incorrect(
                    correct_answer=self.correct_choice_text,
                    explanation=self.explanation,
                ),
                ephemeral=True,
            )
        return await super().callback(interaction)


class AnswerChoices(disnake.ui.View):
    """View that displays answer choices for a question."""

    def __init__(
        self, choices: List[dict], correct_choice_id: int, explanation: str
    ) -> None:
        """Instantiate a new view."""
        super().__init__()
        self.choices = choices
        for choice in self.choices:
            if choice.get("id") == correct_choice_id:
                correct_choice_text = choice.get("text")
                break
        for index, choice in enumerate(self.choices, start=1):
            correct_choice = choice.get("id") == correct_choice_id
            self.add_item(
                AnswerChoice(
                    correct=correct_choice,
                    correct_choice_text=correct_choice_text,
                    choice_id=choice.get("id"),
                    explanation=explanation,
                    label=f"Choice #{index}",
                )
            )
