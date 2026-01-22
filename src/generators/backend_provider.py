# File: backend_provider.py

import importlib
import inspect
from pathlib import Path

from src.common import ProgrammingLanguage
from src.generators.backend import Backend


def get_backend(language: ProgrammingLanguage) -> Backend:
    """
    This function looks for the *Backend class corresponding to the
    provided programming language, and returns an instance of it.

    It only searches this directory ("src/generators"), so any other
    backend added in the future has to be placed here.

    Args:
        language (ProgrammingLanguage): Language name. Has to be in the enum.

    Returns:
        An instance of the retrieved backend class.
    """

    base_import_name = 'src.generators'
    this_directory = Path(__file__).resolve().parent

    files_to_search = [item for item in this_directory.iterdir()
                       if item.is_file() and item.name.endswith('backend.py')]

    for pyfile in files_to_search:
        full_module_name = f'{base_import_name}.{pyfile.stem}'

        try:
            module = importlib.import_module(full_module_name)

            for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
                if vars(class_obj).get('LANGUAGE', None) == language:
                    return class_obj()

        except ImportError:
            continue

    raise ImportError(f'Could not find the backend for language {language}.')
