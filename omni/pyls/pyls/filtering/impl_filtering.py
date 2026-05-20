from pathlib import Path

from pathspec import PathSpec

from .abc_filtering import FilterStrategy


class NoFilter(FilterStrategy):
    def apply(self, path: Path) -> bool:
        _ = path

        return True


class HiddenFilter(FilterStrategy):
    def apply(self, path: Path) -> bool:
        return not path.name.startswith(".")


class PatternFilter(FilterStrategy):
    def __init__(self, patterns: list[str]) -> None:
        self.__spec = PathSpec.from_lines("gitwildmatch", patterns)

    def apply(self, path: Path) -> bool:
        return not self.__spec.match_file(str(path))


class GitIgnoreFilter(FilterStrategy):
    def __init__(self, root: Path) -> None:
        self.__root = root.resolve()

        gitignore = self.__root / ".gitignore"
        if gitignore.exists():
            lines = gitignore.read_text().splitlines()
        else:
            lines = []

        self.__spec = PathSpec.from_lines("gitwildmatch", lines)

    def apply(self, path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(self.__root)
        except ValueError:
            return True  # outside root

        return not self.__spec.match_file(str(relative))


class CompositeFilter(FilterStrategy):
    def __init__(self, *filters: FilterStrategy) -> None:
        self.__filters = filters

    def apply(self, path: Path) -> bool:
        return all(f.apply(path) for f in self.__filters)
