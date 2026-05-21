from typing import TypeVar

ValueType = TypeVar("ValueType")  # pylint: disable=invalid-name


class ValueValidator:
    def __init__(
        self,
        expression: bool,
        exception: Exception,
    ) -> None:
        self.exception = exception
        self.expression = expression

    def validate(self) -> None:
        if not self.expression:
            raise self.exception


class ValueObject[ValueType]:
    def __init__(self, value: ValueType, validators: list[ValueValidator]) -> None:
        self.value = value

        for validator in validators:
            validator.validate()
