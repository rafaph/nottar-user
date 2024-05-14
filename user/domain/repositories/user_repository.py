from abc import ABC, abstractmethod
from collections.abc import Awaitable

from user.domain.models import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retrieve(self, user_id: str) -> Awaitable[User]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retrieve_by_email(self, email: str) -> Awaitable[User]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(self, user: User) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(self, user_id: str) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
