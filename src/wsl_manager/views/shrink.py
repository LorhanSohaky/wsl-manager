from .console import console
from .utils import LowercasePrompt


def display_script_content(script_content: str) -> None:
    console.print("The following script will be executed:")
    console.print("=====================================")
    console.print(script_content)
    console.print("=====================================")
    console.print("")
    LowercasePrompt.get_input(console, "Press any key to continue", False)


def display_shrink_ok() -> None:
    console.print("")
    console.print("[green]Shrink completed successfully![/green]")
