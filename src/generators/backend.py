# File: backend.py

from abc import ABC, abstractmethod
from itertools import zip_longest
from pathlib import Path
from string import Template

from src.utils.common import ProcessResult, ProgrammingLanguage, run_process
from src.models.suite import Suite
from src.utils.text_utils import Color, colorize, print_error


class Backend(ABC):
    """
    The inheriting classes of this class search the appropriate template
    files to generate the runner sources of their respective languages,
    and provide the interfaces to build those sources and execute them.
    """

    LANGUAGE: ProgrammingLanguage
    tester_script: Path

    @abstractmethod
    def get_build_command(self, src: Path) -> str | None:
        pass

    @abstractmethod
    def get_run_command(self) -> str | None:
        pass

    @abstractmethod
    def generate_script(self, suite: Suite) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    def execute_pipeline(self, suite: Suite) -> None:
        """
        Carries out the entire process:
        * Generate the test script
        * Build the script
        * Run the script
        * Set the output of each test case to its corresponding object
          in the suite object.

        Args:
            suite: Object with all the necessary information to generate
                   and run the tests.
        """

        self.generate_script(suite)
        build_result = self._build(suite.source_file_path)

        if build_result is None:
            print_error(
                f'Build tools for {self.LANGUAGE} were not found or could '
                'not be run.'
            )
            return

        if build_result.exit_code != 0:
            print_error(
                'Something went wrong during the build. Check the '
                'error messages output by the build step:\n'
            )

            for line in build_result.output:
                print(colorize(line, Color.LIGHT_RED))
            return

        if not (run_result := self._run()):
            print_error(f'{self.LANGUAGE} was not found or could not be run.')
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
                           if item.is_file() and item.name.startswith(self.LANGUAGE)]

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

    def _build(self, src: Path) -> ProcessResult | None:
        """
        Runs the corresponding tool/compiler on the given source file to build
        it and generate the executable. This command is specified in the
        property build_command by each of the inheriting language classes.

        Returns:
            Exit code from the build tool/compiler (e.g. gcc, g++).
        """

        build_cmd = self.get_build_command(src)

        # We have set the build command to return 'nobuild' for languages that
        # don't need a build to run (e.g. Python, Ruby).
        if build_cmd == 'nobuild':
            return ProcessResult(exit_code=0, output=[], err_pipe=[])

        # If the build tools are not installed, then we return None.
        if build_cmd is None:
            return None

        return run_process(build_cmd)

    def _run(self) -> ProcessResult | None:
        """
        Invokes the given language's runtime to run the generated executable
        with the test cases. Said command is specified by each of the
        inheriting language classes in the run_command property.

        Returns:
            List with the lines printed by the script.
        """

        run_cmd = self.get_run_command()

        # If the language's runtime is not installed, then the run command
        # is represented as None.
        if run_cmd is None:
            return None

        return run_process(run_cmd)
