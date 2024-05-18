from tests.builders.builder import Builder
from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.services import PasswordHasherBuilder

from src.domain.repositories import UserRepository
from src.domain.services import PasswordHasher
from src.domain.use_cases import UpdateUserUseCase


class UpdateUserUseCaseBuilder(Builder[UpdateUserUseCase]):
    def __init__(self) -> None:
        self._user_repository = UserRepositoryBuilder().build()
        self._password_hasher = PasswordHasherBuilder().build()

    def with_user_repository(
        self, user_repository: UserRepository
    ) -> "UpdateUserUseCaseBuilder":
        self._user_repository = user_repository
        return self

    def with_password_hasher(
        self, password_hasher: PasswordHasher
    ) -> "UpdateUserUseCaseBuilder":
        self._password_hasher = password_hasher
        return self

    def build(self) -> UpdateUserUseCase:
        return UpdateUserUseCase(
            self._user_repository,
            self._password_hasher,
        )
