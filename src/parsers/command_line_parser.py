# File: command_line_parser.py

"""
This file contains all the functionality to parse and process the command-line
parameters to the tool.
"""

import argparse


def parse_cmdline() -> dict[str, str]:
    parser = argparse.ArgumentParser(
        description=('A runner tool to test functions easily with multiple '
                     'inputs. Supports multiple languages.')
    )

    parser.add_argument(
        '--config-file',
        type=str,
        required=True
    )

    return vars(parser.parse_args())
