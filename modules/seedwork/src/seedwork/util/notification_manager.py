class NotificationManager:
    def __init__(self):
        self.__errors: list[NotificationErrorProps] = []

    @property
    def errors(self) -> list[NotificationErrorProps]:
        return self.__errors

    def messages(self, context: str) -> str:
        message = ""

        for error in self.__errors:
            if error.context == context:
                message += f"{error.context}: {error.message},"

        return message

    def add_error(self, context: str, message: str) -> None:
        error = NotificationErrorProps(context=context, message=message)
        self.__errors.append(error)

    def has_errors(self) -> bool:
        return len(self.__errors) > 0

    def remove_errors(self) -> None:
        self.__errors.clear()
