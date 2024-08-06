from datetime import datetime
from uuid import UUID, uuid4
from pydantic import Field
from pendulum import now

from base import BaseMixin


class EntityPropsMixin(BaseMixin):
    id: UUID = Field(default_factory=uuid4, allow_mutation=False)
    created_at: datetime = Field(default_factory=now, allow_mutation=False)
    updated_at: datetime = Field(default_factory=now)

    class Config:
        validate_assignment = True
        exclude = ["__props", "__notification", "__events"]
        json_encoders = {datetime: lambda v: v.timestamp()}
