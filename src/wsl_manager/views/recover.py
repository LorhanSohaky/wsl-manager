from pathlib import Path
from typing import Any, Tuple, Union, List

from models import MoveOption
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from .console import console


def display_system_settings() -> MoveOption:
    table = Table(title="Move strategies", show_header=False)
    table.add_column("#", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("Description", justify="left")

    strategies = [
        {
            "id": MoveOption.TAR_FILE,
            "name": "Tar file",
            "description": (
                "[bold green][SAFER AND SLOWER][/bold green] Create a copy of"
                " the system in a tar file and import it from the new path or"
                " disk"
            ),
        },
        {
            "id": MoveOption.WINDOWS_REGISTRY,
            "name": "Windows registry",
            "description": (
                "[bold yellow][FASTER AND LESS SAFE][/bold yellow] Move the"
                " system to another path or disk and update the Windows"
                " registry"
            ),
        },
    ]

    for number, strategy in enumerate(strategies, 1):
        table.add_row(str(number), strategy["name"], strategy["description"])
    console.print(table)

    selected_option = Prompt.ask(
        "Insert the number of the system you want to select",
        choices=[str(number) for number in range(1, len(strategies) + 1)],
        show_choices=False,
    )

    index = int(selected_option) - 1
    selected_strategy = strategies[index]
    return selected_strategy["id"]


def display_select_image_path() -> Path:
    path: Union[None, Path] = None

    while path is None:
        str_path = Prompt.ask("Insert the parent path of VHDX file")
        path = Path(str_path)
        file_path = path / "ext4.vhdx"

        if not file_path.exists():
            console.print("[red]The path not contains an image[/red]")
            path = None
            continue
        elif len(path.suffix) > 0:
            console.print("[red]The path must be a directory[/red]")
            path = None
            continue

        confirmation = Confirm.ask(
            "Do you really want to use this VHDX file"
            f"[bold]{file_path.absolute()}[/bold]?"
        )
        if not confirmation:
            path = None
            continue

    return path

def display_users(list_users: List[Tuple[str,str]]) -> Tuple[str,str]:
    table = Table(title="All Users")
    table.add_column("#", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("UID", justify="center")

    for number, user in enumerate(list_users, 1):
        username, uid = user
        color = "red" if uid == "0" else "green"
        table.add_row(str(number), username, uid, style=color)
    console.print(table)

    selected_option = Prompt.ask(
        "Insert the number of the user you want to select as default",
        choices=[str(number) for number in range(1, len(list_users) + 1)],
        show_choices=False,
    )

    index = int(selected_option) - 1
    return list_users[index]



def display_select_name(already_exist_names: List[str]) -> str:
    name: Union[None, str] = None

    while name is None:
        name = Prompt.ask("Insert the name for the system")

        if name in already_exist_names:
            console.print(
                "[red]The name already exists, please choose another one[/red]"
            )
            name = None
            continue

    return name

def display_moving() -> None:
    console.print("")
    console.print("[yellow]Moving...[/yellow]")
    console.print(
        "Do not close the terminal, shutdown or reboot the system, otherwise"
        " your system could be corrupted."
    )


def display_exporting() -> None:
    console.print("")
    console.print(Text("\tExporting...", tab_size=2))


def display_unregistering() -> None:
    console.print(Text("\tUnregistering...", tab_size=2))


def display_importing() -> None:
    console.print(Text("\tImporting...", tab_size=2))


def display_updating_registry() -> None:
    console.print("")
    console.print(Text("\tUpdating registry...", tab_size=2))


def display_move_ok() -> None:
    console.print("")
    console.print("[green]Moved successfully![/green]")


def display_audit_moving(event: str, args: Tuple[Any, Any]) -> None:
    if event.startswith("shutil") or event.startswith("winreg"):
        console.print(Text(f"\t{event}: {args}", tab_size=4))
