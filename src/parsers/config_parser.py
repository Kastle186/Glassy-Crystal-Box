# File: config_parser

"""
This file contains all the utilities and helpers necessary to validate
and parse the input JSON file, and prepare the objects to run the tests.
"""

import json
from os import PathLike
from pathlib import Path
from typing import Any

from src.utils.common import ConfigField
from src.models.suite import Suite
from src.utils.text_utils import Color, colorize, print_error, print_warning


def setup_tests(json_config_file: str | PathLike) -> list[Suite]:
    """
    This function parses the provided JSON file into the Suite objects
    that this tool uses. It also validates that the provided file contains
    all the necessary information, and fails early if it doesn't. This,
    in order to avoid erratic and inconsistent behavior later on, or
    cryptic error messages.

    Args:
        json_config_file: Path to the JSON file containing the tests'
                          description. (Provided by command-line)

    Returns:
        List of Suite objects with all the processed fields to build and run
        the tests.
    """

    try:
        with open(json_config_file, 'r') as jfile:
            data: dict[str, Any] = json.load(jfile)

    except (OSError, json.JSONDecodeError):
        print_error(f'The file {json_config_file} was not found or could '
                    'not be read correctly.')
        return []

    if base_path_value := data.get(ConfigField.BASE_PATH):
        base_path = Path(base_path_value).expanduser().resolve()
    else:
        base_path = None

    if not (suites_data := data.get(ConfigField.SUITES)):
        print_error(f'The "{ConfigField.SUITES}" field is missing from '
                    'the provided JSON.')
        return []

    result = []

    print('')
    for i, suite_desc in enumerate(suites_data, start=1):
        print(colorize(f'Processing suite #{i}...', Color.CYAN))

        if suite_obj := _parse_suite_data(base_path, suite_desc):
            result.append(suite_obj)

    return result


def _parse_suite_data(base_path: Path | None, suite_desc: dict[str, Any]) -> Suite | None:
    # If "source" was missing or invalid, validate_suite_data() will catch it.
    suite_desc[ConfigField.SOURCE_FILE] = (
        base_path / suite_desc.get(ConfigField.SOURCE_FILE, '')
        if base_path is not None
        else Path(suite_desc.get(ConfigField.SOURCE_FILE, '')).expanduser().resolve()
    )

    if not _validate_suite_data(suite_desc):
        print_warning('Suite description was malformed or is missing data. '
                      'Skipping...')
        return None

    return Suite(suite_desc)


def _validate_suite_data(suite_desc: dict[str, Any]) -> bool:
    errors = []

    source_file = suite_desc.get(ConfigField.SOURCE_FILE)
    function_name = suite_desc.get(ConfigField.FUNCTION_NAME)
    cases = suite_desc.get(ConfigField.TEST_CASES)

    if not source_file or not source_file.is_file():
        errors.append(f'Source file "{source_file}" was not found.')

    if not function_name:
        errors.append('Function name to run is missing.')

    if not cases:
        errors.append('No test cases were found.')
    else:
        for i, case in enumerate(cases, start=1):
            if not case.get(ConfigField.INPUT):
                errors.append(f'Test Case #{i} is missing input arguments.')
            if not case.get(ConfigField.OUTPUT):
                errors.append(f'Test Case #{i} is missing expected output.')

    for err in errors:
        print_error(err)

    return not errors
