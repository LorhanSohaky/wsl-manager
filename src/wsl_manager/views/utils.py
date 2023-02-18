from typing import Optional, TextIO

from rich.console import Console
from rich.prompt import Prompt
from rich.text import TextType


class LowercasePrompt(Prompt):
    @classmethod
    def get_input(
        cls,
        console: Console,
        prompt: TextType,
        password: bool,
        stream: Optional[TextIO] = None,
    ) -> str:
        return (
            super()
            .get_input(
                console=console,
                prompt=prompt,
                password=password,
                stream=stream,
            )
            .lower()
        )
