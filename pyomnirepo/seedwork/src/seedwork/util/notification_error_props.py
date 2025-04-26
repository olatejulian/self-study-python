from .value_object import ValueObject


class NotificationErrorProps(ValueObject):
    context: str
    message: str
