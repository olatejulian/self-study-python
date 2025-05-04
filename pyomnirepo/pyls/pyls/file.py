from datetime import datetime
from pathlib import Path
from typing import TypedDict

from ._exceptions import (
    PathIsNotFileException,
)


class FileDump(TypedDict):
    name: str
    extension: str
    size: int
    path: Path
    is_hidden: bool
    access_date: datetime
    creation_date: datetime
    modification_date: datetime


class File:
    def __init__(self, path: Path):
        File.__validate(path)

        self.__path = path

    @staticmethod
    def __validate(path: Path) -> None:
        expression = path.exists() and path.is_file()

        if not expression:
            raise PathIsNotFileException

    @property
    def name(self) -> str:
        return self.__path.name

    @property
    def extension(self) -> str:
        return self.__path.suffix

    @property
    def size(self) -> int:
        return self.__path.stat().st_size

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def is_hidden(self) -> bool:
        return self.__path.name.startswith(".")

    @property
    def access_date(self) -> datetime:
        access_timestamp = self.__path.stat().st_atime

        access_datetime = datetime.fromtimestamp(access_timestamp)

        return access_datetime

    @property
    def creation_date(self) -> datetime:
        creation_timestamp = self.__path.stat().st_ctime

        creation_datetime = datetime.fromtimestamp(creation_timestamp)

        return creation_datetime

    @property
    def modification_date(self) -> datetime:
        modification_timestamp = self.__path.stat().st_mtime

        modification_datetime = datetime.fromtimestamp(modification_timestamp)

        return modification_datetime

    @property
    def dump(self) -> FileDump:
        return {
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "path": self.path,
            "is_hidden": self.is_hidden,
            "access_date": self.access_date,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
        }
