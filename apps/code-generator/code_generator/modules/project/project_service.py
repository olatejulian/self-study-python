from code_generator.modules.template.application.template_service import (
    TemplateService,
)

from .dto import NewProjectDto
from .project import Project


class ProjectService:
    def __init__(self, template_service: TemplateService):
        self.__template_service = template_service

    def new_project(self, dto: NewProjectDto) -> Project:
        return Project.from_dict(
            {
                "name": dto.project_name,
                "description": dto.description,
                "version": dto.version,
                "author": dto.author,
                "author_email": dto.author_email,
                "template": self.__template_service.get_template_by_name(
                    dto.template_name
                ),
            }
        )
