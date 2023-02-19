from pathlib import Path
from typing import Any, Tuple, Union

from models import MoveOption
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from .console import console


def display_move_options() -> MoveOption:
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


def display_select_path_to_tar_file() -> Path:
    path: Union[None, Path] = None
    while path is None:
        str_path = Prompt.ask("Insert the path to the tar file")
        path = Path(str_path)

        if path.exists():
            console.print("[red]The path already exists[/red]")
            path = None
            continue
        elif path.suffix != ".tar":
            console.print("[red]The file must have the .tar extension[/red]")
            path = None
            continue

        confirmation = Confirm.ask(
            "Do you really want to create the tar file in "
            f"[bold]{path.absolute()}[/bold]?"
        )
        if not confirmation:
            path = None
            continue

    return path


def display_select_path_to_image() -> Path:
    path: Union[None, Path] = None

    while path is None:
        str_path = Prompt.ask("Insert the new path to store the image")
        path = Path(str_path)
        prediction = path / "ext4.vhdx"

        if prediction.exists():
            console.print("[red]The path already contains an image[/red]")
            path = None
            continue
        elif len(path.suffix) > 0:
            console.print("[red]The path must be a directory[/red]")
            path = None
            continue

        confirmation = Confirm.ask(
            "Do you really want to move the image to "
            f"[bold]{path.absolute()}[/bold]?"
        )
        if not confirmation:
            path = None
            continue

    return path


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
