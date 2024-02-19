from rich.prompt import Prompt
from rich.table import Table

from .console import console


def display_menu() -> str:
    table = Table(title="WSL Manager", show_header=False)
    table.add_column("#", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("Description", justify="center")

    options = [
        {
            "id": "shrink",
            "name": "Shrink",
            "description": "Reduce the size of the system",
        },
        {
            "id": "move",
            "name": "Move",
            "description": "Move the system to another path or disk",
        },
        {
            "id": "recover",
            "name": "Recover",
            "description": "Recover a system from a vhdx file",
        },
    ]

    for number, option in enumerate(options, 1):
        table.add_row(str(number), option["name"], option["description"])
    console.print(table)

    selected_option = Prompt.ask(
        "Insert the number of an option",
        choices=[str(number) for number in range(1, len(options) + 1)],
        show_choices=False,
    )

    index = int(selected_option) - 1
    selected_option = options[index]
    return selected_option["id"]
