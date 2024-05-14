from typing import TypeVar

from tests.builders.builder import Builder

T = TypeVar("T")


class BaseUserBuilder(Builder[T]):
    def __init__(self) -> None:
        self._data = {
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "email": self._faker.email(),
            "password": self._faker.password(),
        }

    def with_first_name(self, first_name: str) -> "BaseUserBuilder[T]":
        self._data["first_name"] = first_name
        return self

    def with_last_name(self, last_name: str) -> "BaseUserBuilder[T]":
        self._data["last_name"] = last_name
        return self

    def with_email(self, email: str) -> "BaseUserBuilder[T]":
        self._data["email"] = email
        return self

    def with_password(self, password: str) -> "BaseUserBuilder[T]":
        self._data["password"] = password
        return self
