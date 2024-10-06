from typer import Typer
from video.app import seriesCli


def main():
    video = Typer(name="video")

    video.add_typer(seriesCli)

    return video()


main()
