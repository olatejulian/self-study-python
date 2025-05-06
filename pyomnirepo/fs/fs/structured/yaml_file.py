from typing import Any

import yaml

from ..structured_file import StructuredFile

Data = dict[str, Any]


class YamlFile(StructuredFile[Data]):
    def load(self) -> Data:
        return yaml.safe_load(self.read())

    def dump(self, data: Data) -> None:
        self.write(yaml.safe_dump(data))
