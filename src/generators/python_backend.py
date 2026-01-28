# File: python_backend

import contextlib
import os
import shutil
from pathlib import Path

from src.common import ProgrammingLanguage
from src.generators.backend import Backend
from src.suite import Suite


class PythonBackend(Backend):
    LANGUAGE = ProgrammingLanguage.PYTHON

    def get_build_command(self, src: Path) -> str | None:
        return 'nobuild'

    def get_run_command(self) -> str | None:
        commands = ['py', 'python', 'python3']
        for cmd in commands:
            if shutil.which(cmd):
                return f'{cmd} {self.tester_script}'
        return None

    def generate_script(self, suite: Suite) -> None:
        templates = self.fetch_templates()

        tests = [
            templates['test'].substitute({
                'index': i,
                'function': suite.function_name,
                'args': ', '.join(map(str, tst_case.inputs))
            })
            for i, tst_case in enumerate(suite.tests, start=1)
        ]

        script = templates['main'].substitute({
            'src': suite.source_file_path.as_posix(),
            'function': suite.function_name,
            'test_cases': '\n'.join(tests)
        })

        script_name = 'python_runner.py'
        self.tester_script = Path.cwd() / script_name

        with open(self.tester_script, 'w') as f:
            f.write(f'{script}\n')

    def cleanup(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.tester_script)
