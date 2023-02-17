from dataclasses import dataclass
from typing import List
import re
import subprocess
import functools
import chardet


@dataclass
class RunCommand:
    stdout: str
    returncode: int


def split_by_whitespace(text: str) -> List[str]:
    return re.split(r"\s{2,}", text.strip())


def split_by_line(text: str) -> List[str]:
    return text.split("\n\n")


def parse_table(output) -> List[List[str]]:
    lines = split_by_line(output)
    lines = [split_by_whitespace(line) for line in lines]
    return lines


def detect_encoding(input: bytes) -> str:
    encoding = chardet.detect(input)["encoding"]

    if encoding is None:
        raise Exception("Could not detect encoding")

    return encoding


def run_command(command: str) -> RunCommand:
    output = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    stdout = output.stdout
    decoded_output = stdout.replace("\x00", "")
    return RunCommand(decoded_output, output.returncode)


def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)
