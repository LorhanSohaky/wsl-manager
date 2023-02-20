import sys

import views
from commons.wsl import list_systems, terminate_system
from models import MoveOption

from .strategies import move_using_tar_file, move_using_windows_registry


def move():
    systems = list_systems()
    selected_system = views.display_systems(systems)

    if selected_system.running:
        can_terminate = views.display_warning_to_terminate_system(
            selected_system
        )
        if not can_terminate:
            return

        terminate_system(selected_system)

    strategy = views.display_move_options()

    sys.addaudithook(views.display_audit_moving)
    if strategy == MoveOption.TAR_FILE:
        tar_path = views.display_select_path_to_tar_file()
        image_path = views.display_select_path_to_image()
        views.display_moving()
        move_using_tar_file(selected_system, tar_path, image_path)
    elif strategy == MoveOption.WINDOWS_REGISTRY:
        image_path = views.display_select_path_to_image()
        views.display_moving()
        move_using_windows_registry(selected_system, image_path)
    else:
        raise NotImplementedError("Strategy not implemented")

    views.display_move_ok()
    views.press_any_key_to_continue()
