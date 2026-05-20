from pathlib import Path
from typing import Optional

from rich.console import Console
from typer import Typer
from video.modules import Series, SeriesEpisodeInfoDict

seriesCli = Typer(name="series")


@seriesCli.command()
def rename_episodes(
    series_path: str,
    episode_pattern: Optional[str] = None,
    new_episode_pattern: Optional[str] = None,
    series_name: Optional[str] = None,
):
    console = Console()

    console_err = Console(stderr=True)

    __series_path = Path(series_path)

    __series_name = series_name or __series_path.name

    if not episode_pattern:
        console.print("INSERT EPISODE PATTERN")

        return None

    if not new_episode_pattern:
        console.print("INSERT NEW EPISODE PATTERN")

        return None

    series = Series(
        series_name=__series_name,
        episode_pattern=episode_pattern,
        new_episode_pattern=new_episode_pattern,
    )

    def callback(episode_path: Path, episode_info: SeriesEpisodeInfoDict):
        console.print(
            *(
                [f"Episode File Name: {episode_path.name}"]
                + [f"{key}: {value}" for key, value in episode_info.items()]
            ),
            sep="  \n",
            end="\n\n",
        )

    try:
        path_iterator = series.rename_episodes(__series_path, callback)

        new_series_episodes_paths = list(path_iterator)

    except Exception:
        console_err.print_exception()

    else:
        console.print(new_series_episodes_paths, sep="\n", end="\n\n")

    finally:
        console.print("Done!", highlight=True)
