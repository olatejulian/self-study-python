from __future__ import annotations

import re
from pathlib import Path
from typing import Callable


class NotASubRipFileException(Exception):
    pass


class FloatSecond:
    @staticmethod
    def __validate(seconds: float) -> float:
        seconds = round(seconds, 3)

        if seconds < 0.000:
            raise ValueError

        return seconds

    def __init__(self, seconds: float):
        self.__seconds = self.__validate(seconds)

    def __add__(self, other: FloatSecond | float):
        return FloatSecond(self.__seconds + float(other))

    def __sub__(self, other: FloatSecond | float):
        return FloatSecond(self.__seconds - float(other))

    def __mul__(self, other: FloatSecond | float):
        return FloatSecond(self.__seconds * float(other))

    def __truediv__(self, other: FloatSecond | float):
        return FloatSecond(self.__seconds / float(other))

    def __floordiv__(self, other: FloatSecond | float):
        return FloatSecond(self.__seconds // float(other))

    def __float__(self):
        return float(self.__seconds)

    def __int__(self):
        return int(self.__seconds)

    def __str__(self):
        seconds_str = str(self.__seconds)

        if "." in seconds_str:
            seconds, milliseconds = seconds_str.split(".")

            return f"{seconds}.{milliseconds.ljust(4,'0')}"

        return seconds_str

    def __repr__(self):
        return f"FloatSecond({self.__str__()})"

    @property
    def hours(self) -> int:
        return int(self.__seconds // 3600)

    @property
    def minutes(self) -> int:
        return int((self.__seconds % 3600) // 60)

    @property
    def seconds(self) -> int:
        return int((self.__seconds % 3600) % 60)

    @property
    def milliseconds(self) -> int:
        return int((self.__seconds - int(self.__seconds)) * 1000)


class SubRipFile:
    __default_subtitle_file_extension = ".srt"

    @staticmethod
    def __get_time_in_seconds_from_sub_rip_time_format_str(
        sub_rip_time: re.Match[str],
    ) -> tuple[FloatSecond, FloatSecond]:
        sub_rip_time_format_str_pattern = re.compile(
            r"\d{2}:\d{2}:\d{2},\d{3}"
        )

        sub_rip_time_str = sub_rip_time.group(0)

        all_found_matches = sub_rip_time_format_str_pattern.findall(
            sub_rip_time_str
        )

        def convert_time_str_to_float_seconds(
            time_str: str,
        ) -> FloatSecond:
            hours, minutes, seconds = time_str.split(":")

            seconds_std, milliseconds = seconds.split(",")

            time_in_seconds = (
                float(hours) * 3600
                + float(minutes) * 60
                + float(seconds_std)
                + float(milliseconds) / 1000
            )

            return FloatSecond(time_in_seconds)

        start_time = convert_time_str_to_float_seconds(all_found_matches[0])

        end_time = convert_time_str_to_float_seconds(all_found_matches[1])

        return start_time, end_time

    @staticmethod
    def __convert_seconds_to_sub_rip_time_format_str(
        start_time: FloatSecond, end_time: FloatSecond
    ) -> str:
        def converter(seconds: FloatSecond) -> str:
            return "".join(
                [
                    f"{seconds.hours:02}".zfill(2).ljust(2, "0"),
                    ":",
                    f"{seconds.minutes:02}".zfill(2).ljust(2, "0"),
                    ":",
                    f"{seconds.seconds:02}".zfill(2).ljust(2, "0"),
                    ",",
                    f"{seconds.milliseconds:03}".zfill(3).ljust(3, "0"),
                ]
            )

        start_time_str = converter(start_time)

        end_time_str = converter(end_time)

        return f"{start_time_str} --> {end_time_str}"

    @staticmethod
    def __delay_time(time_s: FloatSecond, delay_s: FloatSecond) -> FloatSecond:
        time_s += delay_s

        return time_s

    @staticmethod
    def __advance_time(
        time_s: FloatSecond, advance_s: FloatSecond
    ) -> FloatSecond:
        time_s -= advance_s

        return time_s

    @classmethod
    def __repl(
        cls,
        advance: FloatSecond | None = None,
        delay: FloatSecond | None = None,
    ) -> Callable[[re.Match[str]], str]:
        def delay_repl(match: re.Match[str], delay: FloatSecond) -> str:
            start_time, end_time = (
                cls.__get_time_in_seconds_from_sub_rip_time_format_str(match)
            )

            start_time = cls.__delay_time(start_time, delay)

            end_time = cls.__delay_time(end_time, delay)

            return cls.__convert_seconds_to_sub_rip_time_format_str(
                start_time, end_time
            )

        def advance_repl(match: re.Match[str], advance: FloatSecond) -> str:
            start_time, end_time = (
                cls.__get_time_in_seconds_from_sub_rip_time_format_str(match)
            )

            start_time = cls.__advance_time(start_time, advance)

            end_time = cls.__advance_time(end_time, advance)

            return cls.__convert_seconds_to_sub_rip_time_format_str(
                start_time, end_time
            )

        if not advance and delay:
            return lambda match: delay_repl(match, delay)

        if advance and not delay:
            return lambda match: advance_repl(match, advance)

        return lambda match: match.group(0)

    @classmethod
    def __validate(cls, path: str) -> Path:
        __path = Path(path)

        if not (
            __path.exists()
            and __path.is_file()
            and __path.suffix == cls.__default_subtitle_file_extension
        ):
            raise NotASubRipFileException

        return __path

    def __init__(self, path: str):
        self.__path = self.__validate(path)

    @staticmethod
    def series_subtitle_name_format(
        name: str, episode: str, locale: str, extension: str
    ) -> str:
        return f"{name}.{episode}.{locale}{extension}"

    def get_language_locale_if_exists(self) -> str | None:
        file_name = self.__path.name

        match = re.search(r"\b([a-z]{2})_([A-Z]{2})\b", file_name)

        return match.group(0) if match else None

    def delay(self, seconds: float) -> None:
        __seconds = FloatSecond(seconds)

        with self.__path.open("r") as subtitle_file:
            text = subtitle_file.read()

            pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"

            text = re.sub(
                pattern=pattern,
                repl=self.__repl(delay=__seconds),
                string=text,
            )

        with self.__path.open("w") as subtitle_file:
            subtitle_file.write(text)

    def advance(self, seconds: float) -> None:
        __seconds = FloatSecond(seconds)

        with self.__path.open("r") as subtitle_file:
            text = subtitle_file.read()

            pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"

            text = re.sub(
                pattern=pattern,
                repl=self.__repl(advance=__seconds),
                string=text,
            )

        with self.__path.open("w") as subtitle_file:
            subtitle_file.write(text)
