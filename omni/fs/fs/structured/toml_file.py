from typing import Any

import toml

from ..structured_file import StructuredFile

Data = dict[str, Any]


class TomlFile(StructuredFile[Data]):
    def load(self) -> Data:
        return toml.loads(self.read())

    def dump(self, data: Data) -> None:
        self.write(toml.dumps(data))
