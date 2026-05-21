from collections.abc import Iterable

from .file import File


class TextFile(File[str]):
    def read(self) -> str:
        return self._path.read_text()

    def write(self, data: str) -> None:
        self._path.write_text(data)

    def append(self, data: str) -> None:
        with self._path.open("a", encoding="utf-8") as f:
            f.write(data)

    def read_lines(self) -> Iterable[str]:
        yield from self._path.read_text("utf-8").splitlines()
