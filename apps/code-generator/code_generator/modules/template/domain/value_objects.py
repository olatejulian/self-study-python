from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Variable(BaseModel):
    name: str


class Target(BaseModel):
    target: str
    kind: Literal["file", "directory"]
    variable: str | None = Field(default=None)
    variables: list[Variable] | None = Field(default=None)


class TemplateMetadata(BaseModel):
    dynamic_targets: list[Target]


class File(BaseModel):
    name: str
    content: bytes


class Directory(BaseModel):
    name: str
    contents: list[Directory | File]
