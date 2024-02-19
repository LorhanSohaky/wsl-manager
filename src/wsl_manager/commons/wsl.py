import re
from itertools import repeat
from pathlib import Path
from typing import Dict, List, TypedDict, Union
from winreg import (
    HKEY_CURRENT_USER,
    KEY_WRITE,
    REG_DWORD,
    REG_SZ,
    CloseKey,
    EnumKey,
    EnumValue,
    OpenKey,
    CreateKey,
    QueryInfoKey,
    HKEYType,
    SetValueEx,
)

from models import System

from .command_line import parse_table, run_command
from .functional import compose

DEFAULT_FLAGS = 15
DEFAULT_VERSION = 2
DEFAULT_STATE = 1


class AdditionalInfo(TypedDict):
    id: str
    base_path: str
    default_user: str


def list_systems() -> List[System]:
    additional_infos = _list_systems_additional_infos()
    output = run_command("wsl -l -v")

    if output.returncode != 0:
        raise Exception("Could not list systems")

    lines = compose(_clean_table, parse_table)(output.stdout)
    content = lines[1:]
    valid_lines = list(filter(lambda x: len(x) == 3, content))

    systems = list(map(_factory_system, repeat(additional_infos), valid_lines))

    return systems


def set_default_user(system: System, user_id: str):
    key = _get_system_key(system)

    registry_key = OpenKey(HKEY_CURRENT_USER, key, 0, KEY_WRITE)
    __set_default_user(registry_key, user_id)
    CloseKey(registry_key)


def create_system(system: System):
    _raise_if_already_exists(system)

    key = _get_system_key(system)
    registry_key = CreateKey(HKEY_CURRENT_USER, key)
    CloseKey(registry_key)
    registry_key = OpenKey(HKEY_CURRENT_USER, key, 0, KEY_WRITE)

    __set_base_path(registry_key, Path(system.base_path))
    __set_default_user(registry_key, system.default_user)
    __set_distribution_name(registry_key, system.name)
    __set_default_metadata(registry_key)

    CloseKey(registry_key)


def update_name_and_default_user(system: System):
    key = _get_system_key(system)
    registry_key = OpenKey(HKEY_CURRENT_USER, key, 0, KEY_WRITE)

    __set_default_user(registry_key, system.default_user)
    __set_distribution_name(registry_key, system.name)

    CloseKey(registry_key)


def set_base_path(system: System, new_image_path: Path):
    key = _get_system_key(system)

    registry_key = OpenKey(HKEY_CURRENT_USER, key, 0, KEY_WRITE)
    __set_base_path(registry_key, new_image_path)
    CloseKey(registry_key)


def terminate_system(system: System):
    output = run_command(f"wsl --terminate {system.name}")

    if output.returncode != 0:
        raise Exception("Could not terminate system")


def _raise_if_already_exists(system: System):
    systems = _list_systems_additional_infos()
    ids = [system["id"] for system in systems.values()]

    if system.id in ids:
        raise Exception("System already exists")


def __set_default_user(registry_key: HKEYType, user_id: int):
    SetValueEx(registry_key, "DefaultUid", 0, REG_DWORD, user_id)


def __set_distribution_name(registry_key: HKEYType, distribution_name: str):
    SetValueEx(registry_key, "DistributionName", 0, REG_SZ, distribution_name)


def __set_default_metadata(registry_key: HKEYType):
    SetValueEx(registry_key, "Flags", 0, REG_DWORD, DEFAULT_FLAGS)
    SetValueEx(registry_key, "Version", 0, REG_DWORD, DEFAULT_VERSION)
    SetValueEx(registry_key, "State", 0, REG_DWORD, DEFAULT_STATE)


def _list_systems_additional_infos() -> Dict[str, AdditionalInfo]:
    regex_keys_systems_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss"

    root = OpenKey(HKEY_CURRENT_USER, regex_keys_systems_path)
    infos = QueryInfoKey(root)
    keys_count = infos[0]

    systems = {}
    for i in range(keys_count):
        subfolder_name = EnumKey(root, i)
        subfolder = OpenKey(root, subfolder_name)
        infos = QueryInfoKey(subfolder)
        values_count = infos[1]

        if not _is_guid(subfolder_name):
            continue

        system_id = subfolder_name
        distribution_name: Union[None, str] = None
        base_path: Union[None, str] = None
        default_user: Union[None, int] = None
        for j in range(values_count):
            name, value, type_ = EnumValue(subfolder, j)
            if name == "DistributionName":
                distribution_name = value
            elif name == "BasePath":
                base_path = value
            elif name == "DefaultUid":
                default_user = value

        if distribution_name is None:
            continue

        systems[distribution_name] = {
            "id": system_id,
            "base_path": base_path,
            "default_user": default_user,
        }

    return systems


def _is_guid(string: str) -> bool:
    return re.match(r"{[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}}", string) is not None


def _clean_table(table: List[List[str]]) -> List[List[str]]:
    new_table = []
    for row in table:
        new_row = []
        for column in row:
            new_row.append(_remove_asterisk_if_present(column).strip())
        new_table.append(new_row)

    return new_table


def _remove_asterisk_if_present(string: str) -> str:
    if string.startswith("*"):
        return string[1:]
    return string


def _factory_system(infos: Dict[str, AdditionalInfo], columns: List[str]) -> System:
    name = columns[0]
    state = columns[1]
    version = columns[2]

    additional_info = infos.get(name)
    if additional_info is None:
        raise Exception(f"Could not find additional info for {name}")

    return System.from_dict(
        {
            "name": name,
            "state": state,
            "version": version,
            "id": additional_info["id"],
            "base_path": additional_info["base_path"],
            "default_user": additional_info["default_user"],
        }
    )


def _get_system_key(system: System):
    return rf"SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss\{system.id}"


def __set_base_path(registry_key: HKEYType, base_path: Path):
    path = str(base_path.absolute())
    SetValueEx(registry_key, "BasePath", 0, REG_SZ, path)
