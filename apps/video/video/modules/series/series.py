import re
from pathlib import Path
from typing import Iterator

from ._types import SeriesEpisodeInfoDict


class Series:
    __episode_file_extensions = [".mkv", ".mp4"]

    __default_zero_padding_length = 2

    def __init__(
        self, series_name: str, episode_pattern: str, new_episode_pattern: str
    ):
        self.__series_name = series_name
        self.__episode_pattern = episode_pattern
        self.__new_episode_pattern = new_episode_pattern

    @property
    def allowed_extensions(self) -> list[str]:
        return self.__episode_file_extensions

    @property
    def zero_padding_length(self) -> int:
        return self.__default_zero_padding_length

    @zero_padding_length.setter
    def zero_padding_length(self, zero_padding_length: int):
        self.__default_zero_padding_length = zero_padding_length

    def rename_episodes(
        self,
        series_directory: Path,
    ) -> Iterator[Path]:
        for episode_path in self.__series_directory_iterator(series_directory):
            if episode_info := self.__get_episode_info(episode_path):
                new_episode_path = self.__rename_episode_file_name(
                    episode_path, episode_info
                )

                yield new_episode_path

    def __verify_episode_file_extension(
        self, episode_file_extension: str
    ) -> bool:
        return episode_file_extension in self.__episode_file_extensions

    def __series_directory_iterator(
        self, series_directory: Path
    ) -> Iterator[Path]:
        if series_directory.is_dir():
            for episode_path in series_directory.iterdir():
                if episode_path.is_file():
                    episode_file_extension = episode_path.suffix

                    if self.__verify_episode_file_extension(
                        episode_file_extension
                    ):
                        yield episode_path

    def __ensure_zero_padding(self, number: int | str) -> str:
        return str(number).zfill(self.__default_zero_padding_length)

    def __get_episode_info(
        self, episode_path: Path
    ) -> SeriesEpisodeInfoDict | None:
        regex = re.compile(self.__episode_pattern)

        episode_file_name = episode_path.stem

        match = regex.match(episode_file_name)

        if not match:
            return None

        groupdict = match.groupdict()

        series_name = self.__series_name

        season_number = self.__ensure_zero_padding(groupdict["season_number"])

        episode_number = self.__ensure_zero_padding(
            groupdict["episode_number"]
        )

        episode_title = groupdict.get("episode_title", "").strip()

        episode_file_extension = episode_path.suffix.replace(".", "")

        episode_info = SeriesEpisodeInfoDict(
            {
                "series_name": series_name,
                "season_number": season_number,
                "number": episode_number,
                "title": episode_title,
                "file_extension": episode_file_extension,
            }
        )

        return episode_info

    def __rename_episode_file_name(
        self,
        episode_path: Path,
        episode_info: SeriesEpisodeInfoDict,
    ) -> Path:
        new_episode_file_name = self.__new_episode_pattern.format(
            **episode_info
        )

        new_episode_path = (
            episode_path.parent / new_episode_file_name
        ).resolve()

        episode_path.rename(new_episode_path)

        return new_episode_path
