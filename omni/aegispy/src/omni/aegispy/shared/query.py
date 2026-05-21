from abc import ABC, abstractmethod
from typing import TypeVar

DataType = TypeVar("DataType")  # pylint: disable=invalid-name


class Query:
    pass


class QueryResponse[DataType]:
    def __init__(self, data: DataType):
        self.data = data


class QueryHandler(ABC):
    @abstractmethod
    async def handle(self, query: Query) -> QueryResponse:
        raise NotImplementedError
