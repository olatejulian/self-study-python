from typing import Callable, TypeVar

from .directory import Directory
from .file import File

TContent = Directory | File

TOutput = TypeVar("TOutput")

TSortByFunctionType = Callable[[Directory | File], TOutput]
