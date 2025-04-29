from abc import ABC, abstractmethod
from datetime import datetime


class TimestampFormatter(ABC):
    @abstractmethod
    def __call__(self, timestamp: float) -> str:
        pass


class DefaultTimestampFormatter:
    __format_scheme = "%Y-%m-%d %H:%M:%S"

    def __init__(self, format_scheme: str | None = None):
        if format_scheme is not None:
            self.__format_scheme = format_scheme

    def __call__(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp)

        datetime_formatted = dt.strftime(self.__format_scheme)

        return datetime_formatted
