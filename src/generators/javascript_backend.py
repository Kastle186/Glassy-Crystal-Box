# File: javascript_backend.py

import shutil
from string import Template

from src.generators.backend import Backend
from src.models.suite import Suite
from src.utils.common import ProgrammingLanguage


class JavascriptBackend(Backend):
    """
    Inheriting Backend class for JavaScript specific functionality.
    """

    def __init__(self):
        self.language = ProgrammingLanguage.JAVASCRIPT
        super().__init__()

    @property
    def run_command(self) -> str | None:
        if shutil.which('node'):
            return f'node {self.tester_script}'
        return None

    def get_and_fill_script_template(
            self,
            templates: dict[str, Template],
            suite: Suite,
            tests: list[str]
    ) -> str:
        return templates['main'].substitute({
            'src': suite.source_file_path.as_posix(),
            'function': suite.function_name,
            'test_cases': '\n'.join(tests)
        })

    def get_and_fill_tests_template(
            self,
            templates: dict[str, Template],
            suite: Suite
    ) -> list[str]:
        return [
            templates['test'].substitute({
                'index': i,
                'args': ', '.join(map(str, tst_case.inputs))
            })
            for i, tst_case in enumerate(suite.tests, start=1)
        ]
