from pydantic import BaseModel


class NewProjectDto(BaseModel):
    project_name: str
    description: str
    author: str
    author_email: str
    version: str
    template_name: str
