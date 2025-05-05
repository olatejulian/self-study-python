from .file import File


class TextFile(File[str]):
    def read(self) -> str:
        return self._path.read_text()

    def write(self, data: str) -> None:
        self._path.write_text(data)
