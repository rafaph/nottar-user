from abc import ABC, abstractmethod

from user.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retrieve(self, user_id: str) -> User:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(self, user_id: str) -> None:
        raise NotImplementedError  # pragma: no cover
