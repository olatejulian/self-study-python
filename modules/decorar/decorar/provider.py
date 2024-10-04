from typing import Callable, Generic, TypeVar

TProvider = TypeVar("TProvider", bound=object)


class Provider(Generic[TProvider]):
    def __init__(self, token: TProvider):
        self.__token = token

    @property
    def token(self) -> TProvider:
        return self.__token


class Factory(Generic[TProvider]):
    def __init__(
        self,
        token: TProvider,
        use_factory: Callable[..., TProvider],
        inject: list[object] = [],
    ):
        self.__token = token
        self.__use_factory = use_factory
        self.__inject = inject

    @property
    def token(self) -> TProvider:
        return self.__token

    def instance(self) -> TProvider:
        return self.__use_factory(*self.__inject)
