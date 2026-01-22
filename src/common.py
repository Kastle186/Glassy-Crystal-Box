# File: common.py

"""
This file contains general utilities used throughout the codebase.
"""

import subprocess
from enum import Enum, StrEnum, auto
from typing import NamedTuple

from src.text_utils import print_critical


class ConfigField(StrEnum):
    BASE_PATH = auto()
    FUNCTION_NAME = auto()
    INPUT = auto()
    OUTPUT = auto()
    SOURCE_FILE = auto()
    SUITES = auto()
    TEST_CASES = auto()


class ProgrammingLanguage(StrEnum):
    C = auto()
    CPP = auto()
    GO = auto()
    JAVA = auto()
    JAVASCRIPT = auto()
    PYTHON = auto()
    RUBY = auto()


class LanguageExtensionMapping(Enum):
    C = ProgrammingLanguage.C
    CPP = ProgrammingLanguage.CPP
    GO = ProgrammingLanguage.GO
    JAVA = ProgrammingLanguage.JAVA
    JS = ProgrammingLanguage.JAVASCRIPT
    MJS = ProgrammingLanguage.JAVASCRIPT
    PY = ProgrammingLanguage.PYTHON
    RB = ProgrammingLanguage.RUBY

    @classmethod
    def from_extension(cls, ext: str) -> ProgrammingLanguage:
        try:
            return cls[ext.upper()].value
        except KeyError:
            print_critical(f'\nFile extension "{ext}" not supported.\n')
            raise


class ProcessResult(NamedTuple):
    exit_code: int
    output: list[str]


def run_process(cmdargs: str | list[str]) -> ProcessResult:
    """
    Runs the received command and returns the process' exit code, alongside
    the output emitted by said process.

    Args:
        cmdargs: String or list of strings containing the name of the
                 file/process to execute, and its arguments to pass.

    Returns:
        ProcessResult named tuple with the exit code and the process' output.
    """

    process = subprocess.Popen(
        args=cmdargs,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, # Get stderr together with stdout.
        text=True,
        bufsize=1
    )

    output_lines = []
    for line in process.stdout:
        output_lines.append(line.rstrip())

    process.wait()
    return ProcessResult(exit_code=process.returncode, output=output_lines)
