from typing import Iterator

from pathspec import PathSpec

from .directory import Directory
from .file import File


class Filter:
    def __init__(self, words: list[str]):
        self.__pathspec = PathSpec.from_lines("gitwildmatch", words)

    def apply(self, directory: Directory) -> Iterator[Directory | File]:
        for content in directory:
            if not self.__pathspec.match_file(
                content.path.relative_to(directory.path)
            ):
                yield content
