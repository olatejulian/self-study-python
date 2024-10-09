from __future__ import annotations

from typing import Self


class MilliSecond:
    MS_IN_SECOND = 1000
    MS_IN_MINUTE = 60 * MS_IN_SECOND
    MS_IN_HOUR = 60 * MS_IN_MINUTE

    @classmethod
    def from_integer(cls, milliseconds: int) -> MilliSecond:
        return cls(milliseconds)

    @classmethod
    def from_string(cls, srt_time: str) -> MilliSecond:
        time_part, ms_part = srt_time.split(",")
        hours, minutes, seconds = map(int, time_part.split(":"))

        total_ms = (
            hours * cls.MS_IN_HOUR
            + minutes * cls.MS_IN_MINUTE
            + seconds * cls.MS_IN_SECOND
            + int(ms_part)
        )

        return cls(total_ms)

    def __init__(self, milliseconds: int):
        self.__milliseconds = milliseconds

    def __add__(self, other: MilliSecond) -> Self:
        self.__milliseconds += other.to_integer()

        return self

    def __sub__(self, other: MilliSecond) -> Self:
        self.__milliseconds -= other.to_integer()

        return self

    def __str__(self) -> str:
        hours = self.__milliseconds // self.MS_IN_HOUR

        minutes = (self.__milliseconds % self.MS_IN_HOUR) // self.MS_IN_MINUTE

        seconds = (
            self.__milliseconds % self.MS_IN_MINUTE
        ) // self.MS_IN_SECOND

        milliseconds = self.__milliseconds % self.MS_IN_SECOND

        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_integer(self) -> int:
        return self.__milliseconds

    def to_string(self) -> str:
        return self.__str__()

    def add(self, other: MilliSecond) -> Self:
        return self + other

    def subtract(self, other: MilliSecond) -> Self:
        return self - other
