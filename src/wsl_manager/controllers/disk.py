import os
from tempfile import NamedTemporaryFile

from models import System

from .utils import run_command


def get_script_content(system: System) -> str:
    return f"""
    select vdisk file="{os.path.join(system.base_path, 'ext4.vhdx')}"
    compact vdisk
    exit
    """


def shrink(script_content: str) -> None:
    script_file = _create_temporary_script_file(script_content)

    output = run_command(f"diskpart /s {script_file}")
    if output.returncode != 0:
        raise Exception("Could not shrink disk")

    os.remove(script_file)


def _create_temporary_script_file(script_content: str) -> str:
    with NamedTemporaryFile(mode="w", delete=False) as file:
        file.write(script_content)

    return file.name
