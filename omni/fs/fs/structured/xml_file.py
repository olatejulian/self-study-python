from typing import Any

import xmltodict

from ..structured_file import StructuredFile

Data = dict[str, Any]


class XmlFile(StructuredFile[Data]):
    def load(self) -> Data:
        return xmltodict.parse(self.read())

    def dump(self, data: Data) -> None:
        self.write(xmltodict.unparse(data))
