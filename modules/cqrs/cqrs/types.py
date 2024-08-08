from typing import Any, Awaitable, Callable

CommandHandler = Callable[[Any], Awaitable[None]]
EventHandler = Callable[[Any], Awaitable[None]]
QueryHandler = Callable[[Any], Awaitable[Any]]
