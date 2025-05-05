from .file import File


class BinaryFile(File[bytes]):
    def read(self) -> bytes:
        return self._path.read_bytes()

    def write(self, data: bytes) -> None:
        self._path.write_bytes(data)
