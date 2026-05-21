from datetime import datetime

from pydantic import EmailStr, SecretStr

from ..utils.all_fields_optional import AllFieldsOptional
from ..utils.app_types import Id
from ..utils.pydantic_base_schema import BaseSchema


class UserSchema(BaseSchema):
    username: str
    email: EmailStr
    name: str


class UserCreate(UserSchema):
    password: SecretStr


class UserUpdate(UserSchema, metaclass=AllFieldsOptional):
    updated_at: datetime | None = datetime.now()


class User(UserSchema):
    id: Id
    updated_at: datetime
    created_at: datetime
