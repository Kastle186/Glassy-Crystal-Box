# File: code_pipeline.py

from src.common import LanguageExtensionMapping, ProgrammingLanguage
from src.generators.backend import Backend
from src.generators.backend_provider import get_backend
from src.suite import Suite


class CodePipeline:
    """
    This class is the core of this tool. It implements calls the backend
    implementation of the source file's language, and generates the temporary
    source file to execute the suite's tests.
    """

    engine_backend: Backend
    language: ProgrammingLanguage
    the_suite: Suite

    def __init__(self, suite: Suite):
        self.language = LanguageExtensionMapping.from_extension(
            suite.source_file_name.split('.')[-1]
        )
        self.the_suite = suite
        self.engine_backend = get_backend(self.language)

    def execute(self):
        self.engine_backend.execute_pipeline(self.the_suite)
        self.the_suite.evaluate_tests()
        print(self.the_suite.to_color_print())
