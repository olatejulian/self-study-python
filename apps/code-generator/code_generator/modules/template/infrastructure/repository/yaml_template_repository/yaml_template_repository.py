from pathlib import Path

import yaml

from ....domain import (
    Directory,
    Template,
    TemplateFileDoesNotExistException,
    TemplateRepository,
)


class YamlTemplateRepository(TemplateRepository):
    def __init__(self, path: str):
        self.__path = path

    def __template_path(self, name: str) -> str:
        template_path = (Path(self.__path) / f"{name}.yaml").absolute()

        template_path.touch(exist_ok=True)

        return str(template_path)

    def save(self, template: Template) -> None:
        with open(self.__template_path(template.name), "w") as file:
            yaml.dump(template.to_dict(), file)

    def get(self, name: str) -> Template:
        try:
            with open(self.__template_path(name), "r") as file:
                yaml_model = yaml.load(file, Loader=yaml.FullLoader)

                template = Template(
                    name=yaml_model["name"],
                    description=yaml_model["description"],
                    main_directory=Directory(**yaml_model["content"]),
                )

        except Exception as e:
            raise TemplateFileDoesNotExistException(e) from e

        else:
            return template

    def delete(self, name: str) -> None:
        Path(self.__template_path(name)).unlink()

    def get_all(self) -> list[Template]:
        path = Path(self.__path)

        return [
            self.get(template.name)
            for template in path.iterdir()
            if template.is_file()
        ]
