from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class UseCase(ABC, Generic[Input, Output]):
    @abstractmethod
    def execute(self, input_: Input) -> Awaitable[Output]:
        raise NotImplementedError  # pragma: no cover
