import json
from typing import Any


class JsonFile:
    @staticmethod
    def read(file_path: str) -> dict[str, Any]:
        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def write(file_path: str, data: dict[str, Any]) -> None:
        with open(file_path, "w") as file:
            json.dump(data, file)
