from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from .millisecond import MilliSecond


class SubRip:
    __time_pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"
    __time_sep = " --> "

    def __init__(self, srt_file_path: str):
        self.__srt_file_path = Path(srt_file_path)

    def shift(self, milliseconds: int):
        __milliseconds = MilliSecond(milliseconds)

        replace_function = self.__repl(milliseconds=__milliseconds)

        subrip_content = self.__srt_file_path.read_text("utf-8")

        replaced_subrip_content = re.sub(
            pattern=self.__time_pattern,
            repl=replace_function,
            string=subrip_content,
        )

        self.__srt_file_path.write_text(
            data=replaced_subrip_content, encoding="utf-8"
        )

    def __repl(
        self, milliseconds: MilliSecond
    ) -> Callable[[re.Match[str]], str]:
        def repl(match: re.Match[str]) -> str:
            time_line = match.group(0)

            start_time_string, end_time_string = time_line.split(
                self.__time_sep
            )

            start_time = MilliSecond.from_string(start_time_string)

            end_time = MilliSecond.from_string(end_time_string)

            start_time += milliseconds

            end_time += milliseconds

            return f"{start_time} --> {end_time}"

        return repl
