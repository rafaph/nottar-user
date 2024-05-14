from tests.builders.builder import Builder
from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.services import PasswordHasherBuilder
from user.domain.repositories import UserRepository
from user.domain.services import PasswordHasher
from user.domain.use_cases import CreateUserUseCase


class CreateUserUseCaseBuilder(Builder[CreateUserUseCase]):
    def __init__(self) -> None:
        self._user_repository = UserRepositoryBuilder().build()
        self._password_hasher = PasswordHasherBuilder().build()

    def with_user_repository(
        self, user_repository: UserRepository
    ) -> "CreateUserUseCaseBuilder":
        self._user_repository = user_repository
        return self

    def with_password_hasher(
        self, password_hasher: PasswordHasher
    ) -> "CreateUserUseCaseBuilder":
        self._password_hasher = password_hasher
        return self

    def build(self) -> CreateUserUseCase:
        return CreateUserUseCase(
            self._user_repository,
            self._password_hasher,
        )
