import shutil
from pathlib import Path


class FileSystem:
    def __init__(self, path: str):
        self.__path = Path(path)

    def __str__(self):
        return str(self.__path)

    def exists(self) -> bool:
        return self.__path.exists()

    def is_dir(self) -> bool:
        return self.__path.is_dir()

    def is_file(self) -> bool:
        return self.__path.is_file()

    def move(self, path: str) -> str:
        return shutil.move(self.__path, Path(path))

    def copy(self, path: str) -> str:
        return shutil.copy2(self.__path, Path(path))
