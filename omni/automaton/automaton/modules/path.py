import os
import shutil
from pathlib import Path


class NotADirectoryException(Exception):
    pass


class NotAFileException(Exception):
    pass


class PathNotExistsException(Exception):
    pass


class CanNotSetFileNameException(Exception):
    pass


def verify_path(path: str):
    if not os.path.exists(path):
        raise PathNotExistsException

    return path


def list_files(path: str):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def list_subdirectories(path: str):
    for subdirectory in os.listdir(path):
        if os.path.isdir(os.path.join(path, subdirectory)):
            yield subdirectory


def set_file_name(path: str, old_name: str, new_name: str):
    try:
        shutil.move(
            os.path.join(path, old_name),
            os.path.join(path, new_name),
        )

    except Exception as e:
        raise CanNotSetFileNameException(e) from e


def get_file_extension(path: str):
    if not os.path.isfile(path):
        raise NotAFileException

    return Path(path).suffix


def get_directory_name(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryException

    return Path(path).stem


def get_file_name(path: str):
    if not os.path.isfile(path):
        raise NotAFileException

    return Path(path).stem


def create_path_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    return path
