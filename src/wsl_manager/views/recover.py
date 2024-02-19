from pathlib import Path
from typing import Union, List

from models import LinuxUser
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .console import console


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


def display_users(list_users: List[LinuxUser]) -> LinuxUser:
    table = Table(title="All Users")
    table.add_column("#", justify="center", no_wrap=True)
    table.add_column("Name", justify="center")
    table.add_column("UID", justify="center")

    for number, user in enumerate(list_users, 1):
        username = user["username"]
        uid = str(user["user_id"])

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


def display_creating_temporary_system() -> None:
    console.print("")
    console.print("[yellow]Creating temporary system...[/yellow]")
    console.print(
        "Do not close the terminal, shutdown or reboot the system, otherwise"
        " your system could be corrupted."
    )

def display_temporary_system_ok() -> None:
    console.print("")
    console.print("[yellow]Temporary system created[/yellow]")

def display_retoring() -> None:
    console.print("")
    console.print("[yellow]Restoring...[/yellow]")
    console.print(
        "Do not close the terminal, shutdown or reboot the system, otherwise"
        " your system could be corrupted."
    )


def display_restore_ok() -> None:
    console.print("")
    console.print("[green]Restored successfully![/green]")
