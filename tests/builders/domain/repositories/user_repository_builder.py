from unittest.mock import AsyncMock, MagicMock

from tests.builders.builder import Builder
from tests.builders.domain.models import UserBuilder
from user.domain.repositories import UserRepository


class UserRepositoryBuilder(Builder[UserRepository]):
    def __init__(self) -> None:
        self._create = AsyncMock(return_value=None)
        self._retrieve = AsyncMock(return_value=UserBuilder().build())
        self._retrieve_by_email = AsyncMock(return_value=UserBuilder().build())
        self._update = AsyncMock(return_value=None)
        self._delete = AsyncMock(return_value=None)

    def with_create(self, create: AsyncMock) -> "UserRepositoryBuilder":
        self._create = create
        return self

    def with_retrieve(self, retrieve: AsyncMock) -> "UserRepositoryBuilder":
        self._retrieve = retrieve
        return self

    def with_retrieve_by_email(
        self, retrieve_by_email: AsyncMock
    ) -> "UserRepositoryBuilder":
        self._retrieve_by_email = retrieve_by_email
        return self

    def with_update(self, update: AsyncMock) -> "UserRepositoryBuilder":
        self._update = update
        return self

    def with_delete(self, delete: AsyncMock) -> "UserRepositoryBuilder":
        self._delete = delete
        return self

    def build(self) -> UserRepository:
        user_repository = MagicMock(spec=UserRepository)
        user_repository.create = self._create
        user_repository.retrieve = self._retrieve
        user_repository.retrieve_by_email = self._retrieve_by_email
        user_repository.update = self._update
        user_repository.delete = self._delete
        return user_repository
