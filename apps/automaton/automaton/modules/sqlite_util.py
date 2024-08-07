import sqlite3
from pathlib import Path

from .path import create_path_if_not_exists


def get_sqlite_connection(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)

    create_path_if_not_exists(str(path.parent.absolute()))

    return sqlite3.connect(db_path)
