import shutil
from pathlib import Path
from typing import Iterator, Self

from .exceptions import DirectoryNotFoundException


class Directory:
    def __init__(self, directory_path: str) -> None:
        self.__path = self.__validate(directory_path)

    def __iter__(self) -> Iterator[Path]:
        return self.__path.iterdir()

    @staticmethod
    def __validate(directory_path: str) -> Path:
        path = Path(directory_path)

        if not path.is_dir():
            raise DirectoryNotFoundException

        return path

    @property
    def name(self) -> str:
        return self.__path.name

    def exists(self) -> bool:
        return self.__path.exists()

    def ls(self) -> Iterator[Path]:
        return self.__path.iterdir()

    def absolute(self) -> Self:
        self.__path = self.__path.absolute()

        return self

    def copy(self, path: str) -> None:
        path_to_copy = Path(path)

        if not path_to_copy.exists():
            path_to_copy.mkdir(parents=True, exist_ok=True)

        shutil.copytree(
            self.__path, path_to_copy, symlinks=True, dirs_exist_ok=True
        )

    def mkdir(self) -> None:
        self.__path.mkdir(parents=True, exist_ok=True)

    def move(self, path: str) -> None:
        path_to_move = Path(path)

        if not path_to_move.exists():
            path_to_move.mkdir(parents=True, exist_ok=True)

        shutil.move(self.__path, path_to_move)

    def rm(self) -> None:
        shutil.rmtree(self.__path)
