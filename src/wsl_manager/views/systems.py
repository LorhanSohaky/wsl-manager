from typing import List

from models import System
from rich.prompt import Prompt
from rich.table import Table

from .console import console
from .utils import LowercasePrompt


def display_systems(systems: List[System]) -> System:
    table = Table(title="All Systems")
    table.add_column("#", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("State", justify="center")

    for number, system in enumerate(systems, 1):
        color = "red" if system.running else "green"
        table.add_row(str(number), system.name, system.state, style=color)
    console.print(table)

    selected_option = Prompt.ask(
        "Insert the number of the system you want to select",
        choices=[str(number) for number in range(1, len(systems) + 1)],
        show_choices=False,
    )

    index = int(selected_option) - 1
    return systems[index]


def display_warning_to_terminate_system(system: System) -> bool:
    console.print(
        "This [bold]system is not terminated[/bold]. To continue, you must"
        " terminate it."
    )
    console.print(
        "[bold red]Remember to close all the programs that are using the"
        " system or it could corrupt the system![/bold red]"
    )
    confirmation = LowercasePrompt.ask(
        f"Are you sure you want to terminate {system.name}?",
        choices=["y", "n", "yes", "no"],
        show_choices=False,
    )

    if confirmation in ["y", "yes"]:
        return True

    console.print("Termination cancelled")
    return False
