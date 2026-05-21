import json
from typing import TypeVar

Data = TypeVar("Data")


class JsonFile[Data]:
    @staticmethod
    def read(file_path: str) -> Data:
        with open(file_path) as file:
            return json.load(file)

    @staticmethod
    def write(file_path: str, data: Data) -> None:
        with open(file_path, "w") as file:
            json.dump(data, file)
