from __future__ import annotations

from pydantic import BaseModel


class File(BaseModel):
    name: str
    content: bytes


class Directory(BaseModel):
    name: str
    contents: list[Directory | File]
