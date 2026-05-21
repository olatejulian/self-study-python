from abc import ABC, abstractmethod
from typing import TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Renderer[Input, Output](ABC):
    @abstractmethod
    def render(self, input: Input) -> Output: ...
