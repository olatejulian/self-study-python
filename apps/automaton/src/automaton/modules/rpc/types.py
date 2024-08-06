from typing import Any, Callable, TypedDict, TypeVar

Handler = Callable[..., Any]


class HandlerInfo(TypedDict):
    name: str
    handler: Handler
    handler_type: type


Handlers = dict[str, HandlerInfo]

UTF8Bytes = bytes

Data = TypeVar("Data")

EncodedData = TypeVar("EncodedData")


class RpcRequestData(TypedDict):
    handler_id: str
    args: list[Any] | tuple[Any]
    kwargs: dict[str, Any]


class RpcResponseData(TypedDict):
    data: Any
