from typer import Typer
from video.modules import SubRip

subtitleCli = Typer(name="subtitle")


@subtitleCli.command()
def shift(srt_file_path: str, milliseconds: int, delay: bool = False):
    if delay:
        milliseconds = -1 * milliseconds

    SubRip(srt_file_path).shift(milliseconds)
