from datetime import datetime
from typing import Union, Optional

from ..utils.app_types import Id
from ..utils.pydantic_base_schema import BaseSchema
from ..utils.all_fields_optional import AllFieldsOptional

class FileMetadataSchema(BaseSchema):
    name: str
    path: str
    public: bool
    url_path: str
    user_id: Id
    expire_at: Optional[Union[datetime, None]]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

class FileMetadataCreate(FileMetadataSchema):
    pass

class FileMetadataUpdate(FileMetadataSchema, metaclass=AllFieldsOptional):
    pass

class FileMetadata(FileMetadataSchema):
    id: Id
