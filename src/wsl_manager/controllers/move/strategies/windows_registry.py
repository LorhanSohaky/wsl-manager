import shutil
from pathlib import Path

import views
from commons.wsl import set_base_path, set_default_user
from models import System


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


def _update_registry(system: System, new_image_path: Path) -> None:
    set_default_user(system, system.default_user)
    set_base_path(system, new_image_path)
