import re


def get_season_episode(filename: str) -> str | None:
    match = re.search(r"\bS(0[1-9]|1[012])E(0[1-9]|[12]\d|3[01])", filename)

    return match.group(0) if match else None


def is_video_file(filename: str) -> bool:
    is_mp4 = filename.endswith(".mp4")

    is_mkv = filename.endswith(".mkv")

    return is_mp4 or is_mkv


def video_name_format(name: str, season_episode: str, extension: str) -> str:
    return f"{name}.{season_episode}{extension}"
