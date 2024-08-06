import re

DEFAULT_SUBTITLE_FILE_EXTENSION = ".srt"


def get_language_locale(filename: str) -> str | None:
    match = re.search(r"\b([a-z]{2})_([A-Z]{2})\b", filename)

    return match.group(0) if match else None


def is_subtitle_file(filename: str) -> bool:
    is_srt = filename.endswith(".srt")

    return is_srt


def subtitle_name_format(
    name: str, episode: str, locale: str, extension: str
) -> str:
    return f"{name}.{episode}.{locale}{extension}"
