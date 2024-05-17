from injector import inject

from src.common import UseCase
from src.domain.errors import UserEmailInUseError, UserNotFoundError
from src.domain.repositories import UserRepository
from src.domain.services import PasswordHasher
from src.domain.use_cases.inputs import CreateUserInput
from src.domain.use_cases.outputs import CreateUserOutput


class CreateUserUseCase(UseCase[CreateUserInput, CreateUserOutput]):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def _user_email_in_use(self, email: str) -> bool:
        try:
            await self._user_repository.retrieve_by_email(email)
        except UserNotFoundError:
            return False
        return True

    async def execute(self, input_: CreateUserInput) -> CreateUserOutput:
        if await self._user_email_in_use(input_.email):
            raise UserEmailInUseError()

        user = input_.to_user(self._password_hasher)

        await self._user_repository.create(user)

        return CreateUserOutput.from_user(user)
