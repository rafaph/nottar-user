from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from faker import Faker

T = TypeVar("T")


class Builder(ABC, Generic[T]):
    _faker = Faker("en_US")

    @abstractmethod
    def build(self) -> T:
        raise NotImplementedError  # pragma: no cover
