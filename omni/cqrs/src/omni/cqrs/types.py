from collections.abc import Awaitable, Callable
from typing import Any

CommandHandler = Callable[[Any], Awaitable[None]]
EventHandler = Callable[[Any], Awaitable[None]]
QueryHandler = Callable[[Any], Awaitable[Any]]
