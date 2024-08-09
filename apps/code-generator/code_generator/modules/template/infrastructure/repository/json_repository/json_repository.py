from pathlib import Path
from typing import Iterator

from code_generator.modules.template import Template, TemplateRepository

from .json_file import JsonFile


class JsonTemplateRepository(TemplateRepository):
    def __init__(self, path: str):
        self.__path = path

    def __template_path(self, name: str) -> str:
        template_path = (Path(self.__path) / f"{name}.json").absolute()

        template_path.touch(exist_ok=True)

        return str(template_path)

    def save(self, template: Template) -> None:
        template_path = self.__template_path(template.name)

        template_dict = template.to_dict()

        JsonFile.write(template_path, template_dict)

    def get(self, name: str) -> Template:
        template_path = self.__template_path(name)

        template_dict = JsonFile.read(template_path)

        template = Template.from_dict(template_dict)

        return template

    def delete(self, name: str) -> None:
        template_path = self.__template_path(name)

        Path(template_path).unlink()

    def get_all(self) -> Iterator[Template]:
        templates_path = Path(self.__path).absolute()

        for path in templates_path.iterdir():
            json_model = path.read_text()

            template = Template.from_json(json_model)

            yield template
