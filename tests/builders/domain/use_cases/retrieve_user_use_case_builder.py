from tests.builders.builder import Builder
from tests.builders.domain.repositories import UserRepositoryBuilder

from src.domain.repositories import UserRepository
from src.domain.use_cases import RetrieveUserUseCase


class RetrieveUserUseCaseBuilder(Builder[RetrieveUserUseCase]):
    def __init__(self) -> None:
        self._user_repository = UserRepositoryBuilder().build()

    def with_user_repository(
        self,
        user_repository: UserRepository,
    ) -> "RetrieveUserUseCaseBuilder":
        self._user_repository = user_repository
        return self

    def build(self) -> RetrieveUserUseCase:
        return RetrieveUserUseCase(self._user_repository)
