import views
from commons.wsl import list_systems, terminate_system

from .disk import disk_shrink, get_script_content


def shrink():
    systems = list_systems()
    selected_system = views.display_systems(systems)

    if selected_system.running:
        can_terminate = views.display_warning_to_terminate_system(
            selected_system
        )
        if not can_terminate:
            return

        terminate_system(selected_system)

    script_content = get_script_content(selected_system)
    views.display_script_content(script_content)
    views.display_shrinking()
    disk_shrink(script_content)
    views.display_shrink_ok()
