from typing import TypedDict


class SeriesEpisodeInfoDict(TypedDict):
    series_name: str
    season_number: str
    episode_number: str
    episode_title: str
    file_extension: str
