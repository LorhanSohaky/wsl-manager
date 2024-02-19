import shutil
from pathlib import Path
from uuid import uuid4

import views
from commons.decorators import raise_if_system_is_running
from commons.wsl import set_base_path, set_default_user
from models import System
from commons.wsl import _list_systems_additional_infos


@raise_if_system_is_running
def move_using_windows_registry(system: System, image_path: Path) -> None:
    image_path.mkdir(parents=True, exist_ok=True)

    _move_image(system, image_path)
    views.display_updating_registry()
    _update_registry(system, image_path)


def _move_image(system: System, image_path: Path) -> None:
    file_name = "ext4.vhdx"
    old_image_path = Path(system.base_path) / file_name
    new_image_path = image_path / file_name

    shutil.move(old_image_path, new_image_path)

    return


def _update_registry(system: System, image_path: Path) -> None:
    set_default_user(system, system.default_user)
    set_base_path(system, new_image_path)


def _generate_system_uuid() -> str:
    all_systems = _list_systems_additional_infos()
    ids = [system["id"] for system in all_systems.values()]

    MAX_TRIES = 100
    tries = 0

    id = str(uuid4())
    while id in ids:
        id = str(uuid4())
        tries += 1
        if tries > MAX_TRIES:
            raise Exception("Could not generate a unique id")
        
    return id
