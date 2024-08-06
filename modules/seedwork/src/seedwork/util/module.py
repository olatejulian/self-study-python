from __future__ import annotations
from functools import reduce
from typing import Any


class Module:
    class Dependency(dict):
        def __init__(self, __dict: dict):
            super().__init__(__dict)

        def __add__(self, other):
            self.update(other)

    imports: list[Any]
    controllers: list[Any]
    providers: list[Any]
    exports: list[Any]

    def __init__(
        self,
        imports: list[Any],
        controllers: list[Any],
        providers: list[Any],
        exports: list[Any],
    ):
        self.imports = imports
        self.controllers = controllers
        self.providers = providers
        self.exports = exports

    def __add__(self, other):
        self.imports += other.imports
        self.controllers += other.controllers
        self.providers += other.providers
        self.exports += other.exports

    @staticmethod
    def add(modules: list[Module]) -> Module:
        s = lambda x, y: x + y

        module = reduce(modules, s)

        return module

    def dependencies(self) -> dict[str, list[Any]]:
        return {
            "imports": self.imports,
            "controllers": self.controllers,
            "providers": self.providers,
            "exports": self.exports,
        }
