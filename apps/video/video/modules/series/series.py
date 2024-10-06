import re
from pathlib import Path
from typing import Iterator

from ._types import SeriesEpisodeInfoDict


class Series:
    __file_extensions = [".mkv", ".mp4"]

    __default_zero_padding_length = 2

    def __init__(
        self, series_name: str, series_episode_pattern: str, new_pattern: str
    ):
        self.__series_name = series_name
        self.__series_episode_pattern = series_episode_pattern
        self.__new_pattern = new_pattern

    @property
    def allowed_extensions(self) -> list[str]:
        return self.__file_extensions

    @property
    def zero_padding_length(self) -> int:
        return self.__default_zero_padding_length

    @zero_padding_length.setter
    def zero_padding_length(self, zero_padding_length: int):
        self.__default_zero_padding_length = zero_padding_length

    def rename_files(self, series_directory: Path) -> Iterator[Path]:
        for series_episode_path in self.__series_directory_iterator(
            series_directory
        ):
            if series_episode_info := self.__get_series_episode_info(
                series_episode_path
            ):
                new_series_episode_path = (
                    self.__rename_series_episode_file_name(
                        series_episode_path, series_episode_info
                    )
                )

                yield new_series_episode_path

    def __verify_series_episode_file_extension(
        self, series_episode_file_extension: str
    ) -> bool:
        return series_episode_file_extension in self.__file_extensions

    def __series_directory_iterator(
        self, series_directory: Path
    ) -> Iterator[Path]:
        if series_directory.is_dir():
            for series_episode_path in series_directory.iterdir():
                if series_episode_path.is_file():
                    series_episode_file_extension = series_episode_path.suffix

                    if self.__verify_series_episode_file_extension(
                        series_episode_file_extension
                    ):
                        yield series_episode_path

    def __ensure_zero_padding(self, number: int | str) -> str:
        return str(number).zfill(self.__default_zero_padding_length)

    def __get_series_episode_info(
        self, series_episode_path: Path
    ) -> SeriesEpisodeInfoDict | None:
        regex = re.compile(self.__series_episode_pattern)

        series_episode_file_name = series_episode_path.stem

        match = regex.match(series_episode_file_name)

        if not match:
            return None

        groupdict = match.groupdict()

        series_name = self.__series_name

        season_number = self.__ensure_zero_padding(groupdict["season_number"])

        episode_number = self.__ensure_zero_padding(
            groupdict["episode_number"]
        )

        episode_title = groupdict.get("episode_title", "").strip()

        series_episode_file_extension = series_episode_path.suffix.replace(
            ".", ""
        )

        series_episode_info = SeriesEpisodeInfoDict(
            {
                "series_name": series_name,
                "season_number": season_number,
                "episode_number": episode_number,
                "episode_title": episode_title,
                "file_extension": series_episode_file_extension,
            }
        )

        return series_episode_info

    def __rename_series_episode_file_name(
        self,
        series_episode_path: Path,
        series_episode_info: SeriesEpisodeInfoDict,
    ) -> Path:
        new_series_episode_file_name = self.__new_pattern.format(
            **series_episode_info
        )

        new_series_episode_path = (
            series_episode_path.parent / new_series_episode_file_name
        ).resolve()

        series_episode_path.rename(new_series_episode_path)

        return new_series_episode_path
