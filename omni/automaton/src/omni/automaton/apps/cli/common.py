import sys
from collections.abc import Callable, Generator
from typing import Any, TypeVar

from rich.console import Console

YieldT = TypeVar("YieldT")

MapperReturnT = TypeVar("MapperReturnT")

console_err = Console(stderr=True)


def generator_handler[YieldT, MapperReturnT](
    generator: Generator[YieldT, Any, Any],
    mapper: Callable[[YieldT], MapperReturnT] | None = None,
):
    result_generator = map(mapper, generator) if mapper else generator

    return list(filter(None, result_generator))


def try_run(func: Callable[..., Any], **kwargs):
    try:
        func(**kwargs)

        sys.exit(0)

    except Exception as e:
        console_err.print(e)

        sys.exit(1)
