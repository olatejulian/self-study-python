from ..domain import (
    DirectoryLoader,
    Template,
    TemplateDict,
    TemplateRepository,
)
from .dto import CreateTemplateDto


class TemplateService:
    def __init__(
        self,
        template_repository: TemplateRepository,
        directory_loader: DirectoryLoader,
    ) -> None:
        self.__template_repository = template_repository
        self.__directory_loader = directory_loader

    def create_from_sample_directory(self, dto: CreateTemplateDto) -> Template:
        template_dict: TemplateDict = {
            "name": dto.template_name,
            "description": dto.template_description,
            "main_directory": self.__directory_loader.load(
                dto.sample_directory_path
            ),
        }

        template = Template.from_dict(template_dict)

        self.__template_repository.save(template)

        return template
