from ..domain import Template, TemplateRepository
from .dto import CreateTemplateDto


class TemplateService:
    def __init__(self, template_repository: TemplateRepository) -> None:
        self.__template_repository = template_repository

    def create(self, dto: CreateTemplateDto) -> Template:
        template = Template(dto)

        self.__template_repository.save(template)

        return template
