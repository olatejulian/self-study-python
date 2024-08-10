from typing import Self, TypedDict

from pydantic import BaseModel, Field

from .value_objects import Directory


class TemplateDict(TypedDict):
    name: str
    description: str
    main_directory: Directory


class TemplateProps(BaseModel):
    name: str = Field(frozen=True)
    description: str
    main_directory: Directory


class Template:
    @classmethod
    def from_dict(cls, dict_model: TemplateDict) -> Self:
        return cls(TemplateProps.model_validate(dict_model))

    @classmethod
    def from_json(cls, json_model: str) -> Self:
        return cls(TemplateProps.model_validate_json(json_model))

    def __init__(self, props: TemplateProps):
        self.__props = props

    @property
    def name(self) -> str:
        return self.__props.name

    def to_dict(self) -> TemplateDict:
        template_dict = self.__props.model_dump()

        return TemplateDict(**template_dict)

    def to_json(self) -> str:
        return self.__props.model_dump_json()
