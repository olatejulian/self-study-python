from typing import Generic, TypeVar, Any

from seedwork.util import NotificationManager, EventManager
from seedwork.abc import AbstractEntity

from entity_props import EntityPropsMixin

Props = TypeVar("Props", bound=EntityPropsMixin)


class EntityMixin(AbstractEntity, Generic[Props]):
    __notification: NotificationManager
    __events: EventManager
    __props: Props

    def __init__(self, props: Props) -> None:
        self.__notification = NotificationManager()
        self.__events = EventManager()
        self.__props = props

    def dict(self) -> dict[str, Any]:
        return self.__props.dict()

    def json(self) -> str:
        return self.__props.json()
