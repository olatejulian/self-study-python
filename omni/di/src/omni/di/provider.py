from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class Provider:
    provides: type[Any]
    use_class: type[Any]
    dependencies: tuple[type[Any], ...]
