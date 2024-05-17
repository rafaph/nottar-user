from tests.builders.builder import Builder
from tests.builders.domain.repositories import UserRepositoryBuilder

from user.domain.repositories import UserRepository
from user.domain.use_cases import DeleteUserUseCase


class DeleteUserUseCaseBuilder(Builder[DeleteUserUseCase]):
    def __init__(self) -> None:
        self._user_repository = UserRepositoryBuilder().build()

    def with_user_repository(
        self, user_repository: UserRepository
    ) -> "DeleteUserUseCaseBuilder":
        self._user_repository = user_repository
        return self

    def build(self) -> DeleteUserUseCase:
        return DeleteUserUseCase(self._user_repository)
