from pathlib import Path

import views
from commons.command_line import RunCommand, run_command
from commons.wsl import set_default_user
from models import System


def move_using_tar_file(
    system: System, tar_path: Path, image_path: Path
) -> None:
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.mkdir(parents=True, exist_ok=True)

    views.display_exporting()
    _export_system(system, tar_path)
    views.display_unregistering()
    _unregister_system(system)
    views.display_importing()
    _import_system(system, tar_path, image_path)
    set_default_user(system, system.default_user)


def _export_system(system: System, tar_path: Path) -> RunCommand:
    output = run_command(f"wsl --export {system.name} {tar_path}")

    if output.returncode != 0:
        raise Exception("Could not export system")

    return output


def _unregister_system(system: System) -> RunCommand:
    output = run_command(f"wsl --unregister {system.name}")

    if output.returncode != 0:
        raise Exception("Could not unregister system")

    return output


def _import_system(
    system: System, tar_path: Path, image_path: Path
) -> RunCommand:
    output = run_command(
        "wsl --import"
        f" {system.name} {image_path.absolute()}"
        f" {tar_path.absolute()} --version {system.version}"
    )

    if output.returncode != 0:
        raise Exception("Could not import system")

    return output
