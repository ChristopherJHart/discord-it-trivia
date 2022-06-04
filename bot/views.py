"""Contains views relevant to trivia questions."""

from typing import List
import disnake


class AnswerChoices(disnake.ui.View):
    """View that displays answer choices for a question."""

    def __init__(self, choices: List[str]) -> None:
        """Instantiate a new view."""
        super().__init__()
        self.choices = choices
        for index, choice in enumerate(self.choices, 1):
            self.add_item(disnake.ui.Button(label=f"{index}: {choice}"))
