from ....modules.subtitle import SubRipFile


class Subtitle:
    @staticmethod
    def delay(subtitle_path: str, delay: float) -> None:
        return SubRipFile(subtitle_path).delay(delay)

    @staticmethod
    def advance(subtitle_path: str, advance: float) -> None:
        return SubRipFile(subtitle_path).advance(advance)
