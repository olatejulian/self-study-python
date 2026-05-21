from collections.abc import Callable
from enum import StrEnum

from .abc_sorting import SortStrategy
from .impl_sorting import (
    CreatedTimeStrategy,
    ExtensionStrategy,
    ModifiedTimeStrategy,
    NameStrategy,
)


class SortToken(StrEnum):
    NAME = "name"
    EXTENSION = "extension"
    CREATED_TIME = "created_time"
    MODIFIED_TIME = "modified_time"


di: dict[SortToken, Callable[..., SortStrategy]] = {
    SortToken.NAME: lambda: NameStrategy(),
    SortToken.EXTENSION: lambda: ExtensionStrategy(),
    SortToken.CREATED_TIME: lambda: CreatedTimeStrategy(),
    SortToken.MODIFIED_TIME: lambda: ModifiedTimeStrategy(),
}


def get_sorter(token: SortToken, *args, **kwargs) -> SortStrategy:
    return di[token](*args, **kwargs)
