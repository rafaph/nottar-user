from injector import inject

from user.common import UseCase
from user.domain.errors import UserEmailInUseError, UserNotFoundError
from user.domain.repositories import UserRepository
from user.domain.services import PasswordHasher
from user.domain.use_cases.inputs import CreateUserInput
from user.domain.use_cases.outputs import CreateUserOutput


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
