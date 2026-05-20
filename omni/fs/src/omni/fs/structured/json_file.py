import json
from typing import Any

from ..structured_file import StructuredFile

Data = dict[str, Any]


class JsonFile(StructuredFile[Data]):
    def load(self) -> Data:
        return json.loads(self.read())

    def dump(self, data: Data) -> None:
        self.write(json.dumps(data))
