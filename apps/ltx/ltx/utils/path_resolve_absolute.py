from pathlib import Path


def PathResolveAbsolute(path: Path) -> Path:
    return path.resolve().absolute()
