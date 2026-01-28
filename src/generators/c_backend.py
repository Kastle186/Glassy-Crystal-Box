# File: c_backend.py

import contextlib
import os
import shutil
from pathlib import Path
from string import Template

from src.common import ProgrammingLanguage
from src.generators.backend import Backend
from src.suite import Suite


class CBackend(Backend):
    """
    Inheriting Backend class for C specific functionality.
    """

    out_file: Path

    def __init__(self):
        self.language = ProgrammingLanguage.C
        super().__init__()

    def get_build_command(self, src: Path) -> str | None:
        # For the time being, we will only support gcc for compiling C files.
        # In the future, we will add other compilers like cl.exe, for example.
        if not shutil.which('gcc'):
            return None

        out_ext = 'exe' if os.name == 'nt' else 'out'
        self.out_file = self.tester_script.parent / f'{self.tester_script.name}.{out_ext}'

        return (
            f'gcc -O2 -std=c18 -Wall -Werror -static '
            f'{src.as_posix()} {self.tester_script.as_posix()} '
            f' -o {self.out_file.as_posix()}'
        )

    def get_run_command(self) -> str | None:
        return self.out_file.as_posix()

    def get_and_fill_script_template(
            self,
            templates: dict[str, Template],
            suite: Suite,
            tests: list[str]
    ) -> str:
        pass

    def get_and_fill_tests_template(
            self,
            templates: dict[str, Template],
            suite: Suite
    ) -> list[str]:
        pass

    def cleanup(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.tester_script)
            os.remove(self.out_file)
