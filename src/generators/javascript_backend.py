# File: javascript_backend

import contextlib
import os
import shutil
from pathlib import Path

from src.common import ProgrammingLanguage
from src.generators.backend import Backend
from src.suite import Suite


class JavascriptBackend(Backend):
    LANGUAGE = ProgrammingLanguage.JAVASCRIPT

    @property
    def build_command(self) -> str | None:
        return 'nobuild'

    @property
    def run_command(self) -> str | None:
        if shutil.which('node'):
            return f'node {self.tester_script}'
        return None

    def generate_script(self, suite: Suite) -> None:
        templates = self.fetch_templates()

        tests = [
            templates['test'].substitute({
                'index': i,
                'args': ', '.join(map(str, tst_case.inputs))
            })
            for i, tst_case in enumerate(suite.tests, start=1)
        ]

        script = templates['main'].substitute({
            'src': suite.source_file_path.as_posix(),
            'function': suite.function_name,
            'test_cases': '\n'.join(tests)
        })

        script_name = 'js_runner.mjs'
        self.tester_script = Path.cwd() / script_name

        with open(self.tester_script, 'w') as f:
            f.write(f'{script}\n')

    def cleanup(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.tester_script)
