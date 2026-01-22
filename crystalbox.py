# File: crystalbox.py

"""
This is the main script that launches the tool.
"""
from src.generators.code_pipeline import CodePipeline
from src.parsers.command_line_parser import parse_cmdline
from src.parsers.config_parser import setup_tests


def main():
    args = parse_cmdline()

    # "--config-file" is marked as required, so we are sure it will always
    # be present.
    the_stuff = setup_tests(args['config_file'])

    for suite in the_stuff:
        codegen = CodePipeline(suite)
        codegen.execute()


if __name__ == '__main__':
    main()
