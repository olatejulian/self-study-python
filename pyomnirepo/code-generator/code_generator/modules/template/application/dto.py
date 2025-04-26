from pydantic import BaseModel


class CreateTemplateDto(BaseModel):
    template_name: str
    template_description: str
    sample_directory_path: str
