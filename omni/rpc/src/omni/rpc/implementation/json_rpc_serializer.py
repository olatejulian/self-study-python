import json

from ..abstracts import RpcClientSerializer, RpcServerSerializer
from ..types import RpcRequestData, RpcResponseData, UTF8Bytes
from ..value_objects import RpcRequest, RpcResponse


class JsonRpcServerSerializer(RpcServerSerializer):
    def encode(self, data: RpcResponse, *args, **kwargs) -> UTF8Bytes:
        return json.dumps(data.do_dict).encode("utf-8")

    def decode(self, encoded_data: UTF8Bytes, *args, **kwargs) -> RpcRequest:
        raw_data: RpcRequestData = json.loads(encoded_data.decode("utf-8"))

        return RpcRequest(**raw_data)


class JsonRpcClientSerializer(RpcClientSerializer):
    def encode(self, data: RpcRequest, *args, **kwargs) -> UTF8Bytes:
        return json.dumps(data.to_dict).encode("utf-8")

    def decode(self, encoded_data: UTF8Bytes, *args, **kwargs) -> RpcResponse:
        raw_data: RpcResponseData = json.loads(encoded_data.decode("utf-8"))

        return RpcResponse(**raw_data)
