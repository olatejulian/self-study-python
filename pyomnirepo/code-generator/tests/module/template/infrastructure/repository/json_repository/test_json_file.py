import json
import os

from code_generator.modules.template import JsonFile


def test_json_file_write():
    file_path = "test.json"

    data = {"key": "value"}

    JsonFile.write(file_path, data)

    with open(file_path, "r") as file:
        assert json.load(file) == data

    os.remove(file_path)


def test_json_file_read():
    file_path = "test.json"

    data = {"key": "value"}

    with open(file_path, "w") as file:
        json.dump(data, file)

    assert JsonFile.read(file_path) == data

    os.remove(file_path)
