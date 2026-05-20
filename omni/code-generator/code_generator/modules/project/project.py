from typing import Self, TypedDict

from pydantic import BaseModel, Field

from code_generator.modules.template import Template


class ProjectDict(TypedDict):
    name: str
    description: str
    version: str
    author: str
    author_email: str
    template: Template


class ProjectProps(BaseModel):
    name: str
    version: str = Field(default="0.1.0")
    description: str
    author: str
    author_email: str
    template: Template


class Project:
    @classmethod
    def from_dict(cls, dict_model: ProjectDict) -> Self:
        return cls(ProjectProps.model_validate(dict_model))

    def __init__(self, props: ProjectProps):
        self.__props = props

    def to_dict(self) -> ProjectDict:
        return ProjectDict(**self.__props.model_dump())
