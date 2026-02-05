# File: backend.py

import contextlib
import os

from abc import ABC, abstractmethod
from itertools import zip_longest
from pathlib import Path
from string import Template

from src.utils.common import (
    LanguageExtensionMapping,
    ProcessResult,
    ProgrammingLanguage,
    run_process
)

from src.models.suite import Suite
from src.utils.text_utils import Color, colorize, print_error


class Backend(ABC):
    """
    The inheriting classes of this class search the appropriate template
    files to generate the runner sources of their respective languages,
    and provide the interfaces to build those sources and execute them.
    """

    language: ProgrammingLanguage
    tester_script: Path


    def __init__(self):
        ext = LanguageExtensionMapping(self.language).name.lower()
        script_name = f'{self.language}_runner.{ext}'
        self.tester_script = Path.cwd() / script_name

    @property
    @abstractmethod
    def run_command(self) -> str | None:
        pass

    @abstractmethod
    def get_and_fill_script_template(
            self,
            templates: dict[str, Template],
            suite: Suite,
            tests: list[str]
    ) -> str:
        pass

    @abstractmethod
    def get_and_fill_tests_template(
            self,
            templates: dict[str, Template],
            suite: Suite
    ) -> list[str]:
        pass

    def setup(self, suite: Suite) -> bool:
        """
        Performs any necessary setup to run the tests. The only essential thing
        to do is to generate the test script. However, compiled languages have
        more steps to follow. Each of their inheriting classes will override
        this base method with their own implementation.

        Args:
            suite: Object with all the necessary information about the source.

        Returns:
            Flag denoting success or failure.
        """

        self.generate_script(suite)
        return True

    def execute(self, suite: Suite):
        """
        Main method in charge of carrying out the backend's workflow:
        * Setup things as needed
        * Generate the test script
        * Build the script
        * Run the script
        * Set the output of each test case to its corresponding object
          in the suite object.

        Args:
            suite: Object with all the necessary information to generate
                   and run the tests.
        """

        if not self.setup(suite):
            print_error(f'{self.language.capitalize()} Backend failed to initialize.')
            return

        if not (run_result := self._run_tester()):
            print_error(f'{self.language} was not found or could not be run.')
            return

            # Set the results to each test, so that the next step in the
            # pipeline can evaluate correctness or failure.

        for test_output, test_case \
                in zip_longest(run_result.output,
                               suite.tests,
                               fillvalue='<missing output>'):
            test_case.stdout = test_output.rstrip() or '<empty>'

        if run_result.err_pipe:
            suite.stderr_lines = run_result.err_pipe

        self.cleanup()

    def cleanup(self) -> None:
        """
        Deletes all the files created to run the tests. Compiled languages also
        generate other object files and whatnot, so they will implement their
        own forms of cleaning up.
        """

        with contextlib.suppress(FileNotFoundError):
            os.remove(self.tester_script)

    def generate_script(self, suite: Suite) -> None:
        """
        Uses the corresponding programming language's template files, and fills
        them up. Then, writes down this new script into its own file.

        Args:
            suite: Object with all the necessary information to generate
                   and run the tests.
        """

        templates = self.fetch_templates()
        tests = self.get_and_fill_tests_template(templates, suite)
        script = self.get_and_fill_script_template(templates, suite, tests)

        with open(self.tester_script, 'w') as f:
            f.write(f'{script}\n')

    def fetch_templates(self) -> dict[str, Template]:
        """
        Searches for the templates corresponding to the specified programming
        language. These templates follow the conventions of Python's Template
        class from the string module, and are each stored in individual files
        under src/templates.

        Returns:
            Dictionary with the type of template as key, and the Template
            object created from the template file as value.
        """

        templates_dir = Path(__file__).resolve().parent.parent / 'templates'
        templates_files = [item for item in templates_dir.iterdir()
                           if item.is_file() and item.name.startswith(self.language)]

        result = {}

        for f in templates_files:
            # All template files follow the convention:
            # <language>.<type>.template
            template_type = f.name.split('.')[1]

            try:
                with open(f, 'r') as temp_f:
                    result[template_type] = Template(temp_f.read())
            except OSError:
                print_error(f'Something went wrong reading template file "{f}".')
                raise

        return result

    def _run_tester(self) -> ProcessResult | None:
        """
        Invokes the given language's runtime to run the generated executable
        with the test cases. Said command is specified by each of the
        inheriting language classes in the run_command property.

        Returns:
            List with the lines printed by the script.
        """

        # If the language's runtime is not installed, then the run command
        # is represented as None.
        if self.run_command is None:
            return None

        return run_process(self.run_command)
