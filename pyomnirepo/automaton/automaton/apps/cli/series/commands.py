from automaton.modules import path as p
from automaton.modules import series as s

from . import types as t


def rename_series_episodes(path: str):
    p.verify_path(path)

    for file_name in p.list_files(path):
        if not s.is_video_file(file_name):
            continue

        if season_episode := s.get_season_episode(file_name):
            try:
                directory_name = p.get_directory_name(path)

                file_extension = p.get_file_extension(path)

                new_file_name = s.video_name_format(
                    directory_name,
                    season_episode,
                    file_extension,
                )

                p.set_file_name(directory_name, file_name, new_file_name)

            except Exception:
                continue

            else:
                yield t.FileData(
                    directory_name=directory_name,
                    file_name=file_name,
                    new_file_name=new_file_name,
                )
