from pathlib import Path
from typing import Optional

from rich.console import Console
from typer import Typer

from ....modules import Series

seriesCli = Typer(name="series")


@seriesCli.command()
def rename_series_episodes(
    series_path: str,
    series_episode_pattern: str,
    new_pattern: str,
    series_name: Optional[str] = None,
):
    console = Console()

    console_err = Console(stderr=True)

    __series_path = Path(series_path)

    __series_name = series_name or __series_path.name

    series = Series(
        series_name=__series_name,
        episode_pattern=series_episode_pattern,
        new_episode_pattern=new_pattern,
    )

    try:
        path_iterator = series.rename_episodes(__series_path)

        new_series_episodes_paths = list(path_iterator)

    except Exception as exc:
        console_err.print(exc)

    else:
        console.print(new_series_episodes_paths, sep="\n", end="\n\n")

    finally:
        console.print("Done!", highlight=True)
