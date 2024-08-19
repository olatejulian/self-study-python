from pathlib import Path
from typing import Callable, Iterator, Literal, TypeVar

from .exceptions import FileNotFoundException, NotAFileException

T = TypeVar("T")


class File:
    def __init__(self, file_path: str) -> None:
        self.__path = self.__validate(file_path)

    def __iter__(self) -> Iterator[str]:
        self.__exists()

        with open(file=self.__path, mode="r", encoding="utf-8") as file:
            while line := file.readline():
                yield line

    @staticmethod
    def __validate(file_path: str) -> Path:
        path = Path(file_path)

        if not path.is_file():
            raise NotAFileException

        return path

    @classmethod
    def read_csv(
        cls,
        csv_file_path: str,
        separator: Literal[",", ";"] = ",",
        header: bool = True,
    ):
        text = cls(csv_file_path).map_over_lines(
            lambda line: [line.strip() for line in line.split(separator)]
        )

        if not header:
            next(text)

        return text

    @property
    def extension(self) -> str:
        return self.__path.suffix

    @property
    def name(self) -> str:
        return self.__path.name

    @property
    def title(self) -> str:
        return self.__path.stem

    def exists(self) -> bool:
        return self.__path.exists()

    def filter_over_lines(self, func: Callable[[str], bool]) -> Iterator[str]:
        for line in self:
            if func(line):
                yield line

    def map_over_lines(self, func: Callable[[str], T]) -> Iterator[T]:
        for line in self:
            yield func(line)

    def read(self, mode: Literal["r", "rb"] = "r") -> str | bytes:
        self.__exists()

        match mode:
            case "r":
                return self.__path.read_text()

            case "rb":
                return self.__path.read_bytes()

            case _:
                raise ValueError

    def touch(self) -> None:
        self.__path.touch(exist_ok=True)

    def write(self, data: str | bytes) -> None:
        if isinstance(data, str):
            self.__path.write_text(data)

        if isinstance(data, bytes):
            self.__path.write_bytes(data)

    def __exists(self) -> None:
        if not self.exists():
            raise FileNotFoundException
