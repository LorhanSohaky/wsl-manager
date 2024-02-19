import re

from typing import List
from pathlib import Path

import views.recover as views

from commons.wsl import (
    terminate_system,
    create_system,
    _list_systems_additional_infos,
    update_name_and_default_user,
)
from commons.command_line import run_command
from models import System, LinuxUser
from views import press_any_key_to_continue

from .windows_registry import _generate_system_uuid, _generate_system_uuid


def recover():
    image_path = views.display_select_image_path()

    views.display_creating_temporary_system()
    temporary_system = _create_temporary_system(image_path)
    views.display_temporary_system_ok()

    system_name = select_system_name()
    selected_default_user = select_default_user(temporary_system.name)

    views.display_retoring()
    terminate_system(temporary_system)
    system = System.from_dict(
        {
            "id": temporary_system.id,
            "name": system_name,
            "base_path": str(image_path.absolute()),
            "default_user": selected_default_user["user_id"],
            "version": "2",
        }
    )

    update_name_and_default_user(system)
    views.display_restore_ok()

    press_any_key_to_continue()


def _create_temporary_system(base_path: Path) -> System:
    id = _generate_system_uuid()

    system = System.from_dict(
        {
            "id": "{" + id + "}",
            "name": id,
            "base_path": str(base_path.absolute()),
            "default_user": 0,
            "version": "2",
        }
    )

    create_system(system)
    return system


def select_system_name() -> str:
    all_systems = _list_systems_additional_infos()
    system_names = [name for name in all_systems.keys()]
    selected_name = views.display_select_name(system_names)

    return selected_name


def select_default_user(system_name: str) -> LinuxUser:
    uid_min = _get_min_uid(system_name)
    list_users = _detect_users(system_name, uid_min)

    selected_default_user = views.display_users(list_users)
    return selected_default_user


def _get_min_uid(system_name: str) -> int:
    output = run_command(
        f"wsl -d {system_name} sh -c 'grep \"^UID_MIN\" /etc/login.defs'"
    )

    if output.returncode != 0:
        raise Exception("Could not detect UID_MIN in the system")

    match = re.search(r"UID_MIN\s+(\d+)", output.stdout)
    if not match:
        raise Exception("Could not detect UID_MIN in the system")
    uid_min = match.group(1)

    return int(uid_min)


def _detect_users(system_name: str, uid_min: int) -> List[LinuxUser]:
    output = run_command(f"wsl -d {system_name} sh -c 'cat /etc/passwd'")

    if output.returncode != 0:
        raise Exception("Could not detect existing users in the system")

    matches = re.finditer(
        r"^(.+?):(.+?):(.+?):(.+?)?:(.+?)?:(.+?):(.+?)$", output.stdout, re.MULTILINE
    )

    list_users: List[LinuxUser] = [{"username": "root", "user_id": 0}]
    for match in matches:
        user_id = match.group(3)
        if int(user_id) < uid_min:
            continue

        username = match.group(1)
        list_users.append({"username": username, "user_id": int(user_id)})

    return list_users
