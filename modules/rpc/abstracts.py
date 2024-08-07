from abc import ABC, abstractmethod
from typing import Generic

from .types import Data, EncodedData, UTF8Bytes
from .value_objects import RpcRequest, RpcResponse


class Encoder(ABC, Generic[Data, EncodedData]):
    @abstractmethod
    def encode(self, data: Data, *args, **kwargs) -> EncodedData:
        raise NotImplementedError


class Decoder(ABC, Generic[Data, EncodedData]):
    @abstractmethod
    def decode(self, encoded_data: EncodedData, *args, **kwargs) -> Data:
        raise NotImplementedError


class RpcServerSerializer(
    Encoder[RpcResponse, UTF8Bytes], Decoder[RpcRequest, UTF8Bytes], ABC
):
    pass


class RpcClientSerializer(
    Encoder[RpcRequest, UTF8Bytes], Decoder[RpcResponse, UTF8Bytes], ABC
):
    pass
