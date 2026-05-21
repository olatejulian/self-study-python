from datetime import datetime

from ..utils.all_fields_optional import AllFieldsOptional
from ..utils.app_types import Id
from ..utils.pydantic_base_schema import BaseSchema


class FileMetadataSchema(BaseSchema):
    name: str
    path: str
    public: bool
    url_path: str
    user_id: Id
    expire_at: datetime | None | None
    updated_at: datetime | None
    created_at: datetime | None


class FileMetadataCreate(FileMetadataSchema):
    pass


class FileMetadataUpdate(FileMetadataSchema, metaclass=AllFieldsOptional):
    pass


class FileMetadata(FileMetadataSchema):
    id: Id
