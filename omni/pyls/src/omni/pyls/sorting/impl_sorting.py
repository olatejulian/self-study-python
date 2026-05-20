from pathlib import Path

from .abc_sorting import SortStrategy


class NameStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return path.name.casefold()


class ExtensionStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return path.suffix.casefold()


class CreatedTimeStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return str(path.stat().st_ctime)


class ModifiedTimeStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return str(path.stat().st_mtime)
