from pathlib import Path
from typing import Protocol


class FilterStrategy(Protocol):
    def apply(self, path: Path) -> bool: ...
