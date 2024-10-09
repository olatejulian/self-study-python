from typer import Typer
from video.app import seriesCli, subtitleCli


def main():
    video = Typer(name="video")

    video.add_typer(seriesCli)

    video.add_typer(subtitleCli)

    return video()


main()
