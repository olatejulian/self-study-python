from seedwork.type import Event


class EventManager:
    def __init__(self):
        self.__events: list[Event]

    @property
    def events(self) -> list[Event]:
        return self.__events

    def add_event(self, event: Event) -> None:
        self.__events.append(event)

    def delete_events(self) -> None:
        self.__events.clear()
