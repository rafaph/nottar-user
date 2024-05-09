from abc import ABC, abstractmethod

from user.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
        raise NotImplementedError
