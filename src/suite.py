# File: suite.py

"""
This file contains the models to store all the data related to test cases,
runs, and their results.
"""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar

from src.common import ConfigField
from src.text_utils import Color, colorize, make_banner


class TestStatus(StrEnum):
    PASSED = 'Passed'
    FAILED = 'Failed'
    NOT_RUN = 'Not Run'


@dataclass
class TestCaseDescription:
    """
    A dataclass containing all the information related to a specific test
    case, from a specific suite.

    Attributes:
        test_id (int): Unique identifier for reporting and finding the test.
        inputs: (list[Any]): Arguments to pass to the function to test.
        expected_output (str): String expected to be printed when running the test.
        stdout (str | None): Actual data printed to stdout.
        stderr (str | None): Error data printed to stderr (if any).
        status (TestStatus): Current status of the test case.
    """

    _status_colors_field: ClassVar[dict[TestStatus, Color]] = {
        TestStatus.PASSED: Color.LIGHT_GREEN,
        TestStatus.FAILED: Color.LIGHT_RED,
        TestStatus.NOT_RUN: Color.LIGHT_YELLOW
    }

    test_id: int
    inputs: list[Any]
    expected_output: str
    stdout: str | None = None
    stderr: str | None = None
    status: TestStatus = TestStatus.NOT_RUN

    def __post_init__(self):
        self.expected_output = str(self.expected_output)

    @property
    def _status_colors(self) -> dict[TestStatus, Color]:
        return self._status_colors_field

    def evaluate(self) -> None:
        self.status = (TestStatus.PASSED if self.stdout == self.expected_output
                       else TestStatus.FAILED)

    def to_color_string(self) -> str:
        lines = [
            make_banner(f'Test #{self.test_id}', '-', Color.LIGHT_MAGENTA),
            '',
            f'{colorize("Input Params:", Color.YELLOW)} {", ".join(map(str, self.inputs))}',
            colorize(f'Test {self.status}!', self._status_colors[self.status])
        ]

        if self.status is TestStatus.FAILED:
            lines.append(self._get_expected_vs_actual_string())

        if self.stderr:
            lines.append(self._get_stderr_string())

        return '\n'.join(lines)

    def _get_expected_vs_actual_string(self) -> str:
        return (
            f'{colorize("Expected:", Color.LIGHT_RED)} {self.expected_output}\n'
            f'{colorize("Actual:", Color.LIGHT_RED)} {self.stdout}'
        )

    def _get_stderr_string(self) -> str:
        return (
            f'{colorize("There were also other errors:", Color.RED)}\n\n'
            f'{colorize(self.stderr, Color.RED)}'
        )


class Suite:
    """
    A class containing the list of test cases to run against a specific
    function, in a specific file.

    Attributes:
        source_file_path (Path): Full path to the source code file to run.
        function_name (str): Function to run the test cases against.
        tests (list[TestCaseDescription]): List of test cases to run.
    """

    source_file_path: Path
    function_name: str
    stderr_lines: list[str] | None
    tests: list[TestCaseDescription]

    passed: int
    failed: int
    not_run: int

    def __init__(self, suite_data: dict[str, Any]):
        # At this point, all the data has already been validated that it
        # exists, and "source_file" has been converted to "Path".
        self.source_file_path = suite_data[ConfigField.SOURCE_FILE]
        self.function_name = suite_data[ConfigField.FUNCTION_NAME]
        self.stderr = None

        self.tests = [
            TestCaseDescription(
                test_id=i,
                inputs=test_data[ConfigField.INPUT],
                expected_output=test_data[ConfigField.OUTPUT]
            )
            for i, test_data in enumerate(suite_data[ConfigField.TEST_CASES],
                                          start=1)
        ]

        self.passed = 0
        self.failed = 0
        self.not_run = 0

    @property
    def source_file_name(self) -> str:
        return self.source_file_path.name

    def evaluate_tests(self) -> None:
        for tc in self.tests:
            tc.evaluate()

            if tc.status is TestStatus.PASSED:
                self.passed += 1
            elif tc.status is TestStatus.FAILED:
                self.failed += 1
            elif tc.status is TestStatus.NOT_RUN:
                self.not_run += 1

    def to_color_print(self) -> str:
        lines = [
            '\n',
            make_banner(f'Suite of {self.source_file_name}', '*', Color.LIGHT_BLUE),
            colorize(f'\nFunction executed: {self.function_name}', Color.CYAN),
            '',
            '\n\n'.join(tc.to_color_string() for tc in self.tests),
            '',
            make_banner('Suite Summary', '=', Color.LIGHT_CYAN),
            colorize(f'\nPassed: {self.passed}', Color.LIGHT_GREEN),
            colorize(f'Failed: {self.failed}', Color.LIGHT_RED),
            colorize(f'Not Run: {self.not_run}', Color.LIGHT_YELLOW)
        ]

        if self.stderr_lines:
            lines.extend([
                '',
                make_banner('Errors', '=', Color.RED),
                '',
                '\n'.join(colorize(line, Color.RED) for line in self.stderr_lines)
            ])

        return '\n'.join(lines)
