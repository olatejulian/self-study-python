from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterator, TypedDict

from .file import File


class NotADirectoryException(Exception):
    pass


class DirectoryDump(TypedDict):
    name: str
    path: Path
    is_hidden: bool
    access_date: datetime
    creation_date: datetime
    modification_date: datetime


class Directory:
    @staticmethod
    def __validate(path: Path) -> None:
        expression = path.exists() and path.is_dir()

        if not expression:
            raise NotADirectoryException()

    def __init__(self, path: Path):
        Directory.__validate(path)

        self.__path = path

    def __iter__(self) -> Iterator[Directory | File]:
        generator = self.__path.iterdir()

        for content_path in generator:
            if content_path.is_dir():
                yield Directory(content_path)

            if content_path.is_file():
                yield File(content_path)

    @property
    def name(self) -> str:
        return self.__path.name

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
    def dump(self) -> DirectoryDump:
        return {
            "name": self.name,
            "path": self.path,
            "is_hidden": self.is_hidden,
            "access_date": self.access_date,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
        }
