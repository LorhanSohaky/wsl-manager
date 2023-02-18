from typing import List

from models import System
from rich.prompt import Prompt
from rich.table import Table

from .console import console


def display_systems(systems: List[System]) -> System:
    table = Table(title="All Systems")
    table.add_column("nº", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("State", justify="center")

    for number, system in enumerate(systems, 1):
        color = "green" if system.state == "Stopped" else "red"
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
    is_valid_confirmation = False
    while is_valid_confirmation is False:
        print(
            "This system is not terminated. To continue, you must"
            " terminate it."
        )
        print(f"Are you sure you want to terminate {system.name}? (y/n)")

        confirmation = input("Confirmation: ").lower()
        is_valid_confirmation = confirmation in ["yes", "y", "no", "n"]
        if not is_valid_confirmation:
            print("Invalid confirmation")
            continue

        if confirmation not in ["yes", "y"]:
            print("Termination cancelled")
            return False

    return True
