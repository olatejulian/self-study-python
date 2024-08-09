from typing import Any

from pydantic import BaseModel, Field

from .value_objects import Directory


class TemplateProps(BaseModel):
    name: str = Field(frozen=True)
    description: str
    main_directory: Directory


class Template:
    @classmethod
    def from_dict(cls, dict_model: dict[str, Any]):
        return cls(TemplateProps.model_validate(dict_model))

    @classmethod
    def from_json(cls, json_model: str):
        return cls(TemplateProps.model_validate_json(json_model))

    def __init__(self, props: TemplateProps):
        self.__props = props

    @property
    def name(self) -> str:
        return self.__props.name

    def to_dict(self) -> dict[str, Any]:
        return self.__props.model_dump()

    def to_json(self) -> str:
        return self.__props.model_dump_json()
