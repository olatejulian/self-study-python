from pathlib import Path
from typing import TypedDict


class LtxConfigDirsDict(TypedDict):
    root: str
    build: str
    output: str
    resources: str
    source: str


class LtxConfigDict(TypedDict):
    dirs: LtxConfigDirsDict
    args: list[str]


class LtxConfigDirPathsDict(TypedDict):
    root: Path
    build: Path
    output: Path
    resources: Path
    source: Path
