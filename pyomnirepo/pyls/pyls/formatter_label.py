from abc import ABC, abstractmethod
from enum import StrEnum

from .directory import Directory
from .file import File


class LabelFormatter(ABC):
    @abstractmethod
    def format_directory_label(self, directory: Directory) -> str: ...

    @abstractmethod
    def format_file_label(self, file: File) -> str: ...


class LabelFormatterStyle(StrEnum):
    SIMPLE = "simple"


class LabelFormatterFactory:
    @staticmethod
    def create(style: LabelFormatterStyle) -> LabelFormatter:
        formatters = {
            LabelFormatterStyle.SIMPLE: SimpleLabelFormatter(),
        }

        return formatters[style]


class SimpleLabelFormatter(LabelFormatter):
    def format_directory_label(self, directory: Directory) -> str:
        return f"📁 [bold green]{directory.name}[/]"

    def format_file_label(self, file: File) -> str:
        return f"📄 {file.name}"
