import re
from itertools import repeat
from typing import Dict, List, TypedDict
from winreg import HKEY_CURRENT_USER, EnumKey, EnumValue, OpenKey, QueryInfoKey

from models import System

from .utils import compose, parse_table, run_command


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


class AdditionalInfo(TypedDict):
    id: str
    base_path: str


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
        distribution_name = None
        base_path = None
        for j in range(values_count):
            name, value, type_ = EnumValue(subfolder, j)
            if name == "DistributionName":
                distribution_name = value
            elif name == "BasePath":
                base_path = value

        if distribution_name is None:
            continue

        systems[distribution_name] = {
            "id": system_id,
            "base_path": base_path,
        }

    return systems


def _is_guid(string: str) -> bool:
    return (
        re.match(r"{[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}}", string)
        is not None
    )


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


def _factory_system(
    infos: Dict[str, AdditionalInfo], columns: List[str]
) -> System:
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
        }
    )


def terminate_system(system: System):
    output = run_command(f"wsl --terminate {system.name}")

    if output.returncode != 0:
        raise Exception("Could not terminate system")
