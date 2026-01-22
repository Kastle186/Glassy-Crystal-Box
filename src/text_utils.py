# File: text_utils.py

"""
This file contains the utilities and helpers for processing text to print,
namely formatting and colorizing it.
"""

from enum import StrEnum
from typing import Any

import colorama

colorama.init(autoreset=True)
Fore = colorama.Fore


class Color(StrEnum):
    DEFAULT = Fore.RESET

    BLACK = Fore.BLACK
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    MAGENTA = Fore.MAGENTA
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    WHITE = Fore.WHITE

    LIGHT_BLACK = Fore.LIGHTBLACK_EX
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    LIGHT_CYAN = Fore.LIGHTCYAN_EX
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    LIGHT_RED = Fore.LIGHTRED_EX
    LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    LIGHT_WHITE = Fore.LIGHTWHITE_EX


def colorize(item: Any, color: Color) -> str:
    return (
        f'{color}{item}{Color.DEFAULT}'
        if color is not Color.DEFAULT
        else f'{item}'
    )


def make_banner(text: str, banner_char: str, color: Color = Color.DEFAULT) -> str:
    # Adding +4 here to take into account the chars/spaces surrounding
    # the text in the banner.
    banner_len = len(text) + 4
    banner_border = banner_char * banner_len

    return colorize(
        f'{banner_border}\n{banner_char} {text} {banner_char}\n{banner_border}',
        color
    )


def print_critical(msg: str) -> None:
    print(colorize(f'TOOL ERROR: {msg}', Color.RED))


def print_error(msg: str) -> None:
    print(colorize(f'ERROR: {msg}.', Color.LIGHT_RED))


def print_warning(msg: str) -> None:
    print(colorize(f'WARNING: {msg}.', Color.LIGHT_YELLOW))
