from ..value_object import NotificationErrorProps


class NotificationError(Exception):
    def __init__(self, errors: list[NotificationErrorProps]):
        super().__init__()
