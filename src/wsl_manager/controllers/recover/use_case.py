import sys
from typing import List, Tuple
import views.recover as views
from views import press_any_key_to_continue
from commons.wsl import list_systems, terminate_system, create_system, _list_systems_additional_infos, update_name_and_default_user
from models import MoveOption, System

from pathlib import Path
from .windows_registry import _generate_system_uuid, move_using_windows_registry, _generate_system_uuid
from commons.command_line import run_command
import re


def recover():
    image_path = views.display_select_image_path()

    temporary_system = _create_temporary_system(image_path)

    # get user ids
    output = run_command(f"wsl -d {temporary_system.name} sh -c 'grep \"^UID_MIN\" /etc/login.defs'")

    if output.returncode != 0:
        raise Exception("Could not detect UID_MIN in the system")
    
    match = re.search(r"UID_MIN\s+(\d+)", output.stdout)
    if not match:
        raise Exception("Could not detect UID_MIN in the system")
    uid_min = match.group(1)

    output = run_command(f"wsl -d {temporary_system.name} sh -c 'cat /etc/passwd'")

    if output.returncode != 0:
        raise Exception("Could not detect existing users in the system")
    
    matches = re.finditer(r"^(.+?):(.+?):(.+?):(.+?)?:(.+?)?:(.+?):(.+?)$", output.stdout, re.MULTILINE)


    list_users: List[Tuple[str,str]] = [("root", "0")]
    for match in matches:
        user_id = match.group(3)
        if int(user_id) < int(uid_min):
            continue
        
        username = match.group(1)
        list_users.append((username, user_id))


    all_systems = _list_systems_additional_infos()
    system_names = [name for name in all_systems.keys()]
    selected_name = views.display_select_name(system_names)

    selected_default_user = views.display_users(list_users)

    terminate_system(temporary_system)
    
    system = System(
        id=temporary_system.id,
        name=selected_name,
        base_path=str(image_path.absolute()),
        default_user=selected_default_user[1],
        state="Stopped",
        version="2",
    )

    update_name_and_default_user(system)

    
    press_any_key_to_continue()

def _create_temporary_system(base_path: Path) -> System:
    id = _generate_system_uuid()

    system = System(
        id="{" + id + "}",
        name=id,
        base_path=str(base_path.absolute()),
        default_user="0", # root
        state="Stopped",
        version="2",
    )

    create_system(system)
    return system
