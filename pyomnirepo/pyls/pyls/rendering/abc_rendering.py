from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Renderer(ABC, Generic[Input, Output]):
    @abstractmethod
    def render(self, input: Input) -> Output: ...
