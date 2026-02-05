# File: compiled_backend.py

from abc import ABC

from src.generators.backend import Backend


class CompiledBackend(Backend, ABC):
    """
    Compiled languages like Java and C/C++ have some extra steps before we can
    run them. This class provides the contract for said steps, so each of the
    languages' inheriting classes can implement it accordingly.
    """
    pass
