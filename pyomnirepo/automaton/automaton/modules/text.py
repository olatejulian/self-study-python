from typing import Callable, Iterator, TypeVar

from ..modules import path as p

T = TypeVar("T")


class Text:
    def __init__(self, text_file_path: str):
        self.__text_path = p.verify_path(text_file_path)

    def __iter__(self):
        with open(
            file=self.__text_path, mode="r", encoding="utf-8"
        ) as text_file:
            while line := text_file.readline():
                yield line

    def map(self, func: Callable[[str], T]) -> Iterator[T]:
        for line in self:
            yield func(line)

    def filter(self, func: Callable[[str], bool]) -> Iterator[str]:
        for line in self:
            if func(line):
                yield line

    @classmethod
    def read_csv(
        cls, csv_file_path: str, separator: str = ",", drop_header=False
    ):
        text = cls(csv_file_path).map(
            lambda line: [line.strip() for line in line.split(separator)]
        )

        if drop_header:
            next(text)

        return text
