from injector import inject

from user.common import UseCase
from user.domain.errors import UserNotFoundError
from user.domain.repositories import UserRepository
from user.domain.services import PasswordHasher
from user.domain.use_cases.inputs import VerifyUserInput
from user.domain.use_cases.outputs import VerifyUserOutput


class VerifyUserUseCase(UseCase[VerifyUserInput, VerifyUserOutput]):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, input_: VerifyUserInput) -> VerifyUserOutput:
        user = await self._user_repository.retrieve_by_email(input_.email)

        hash_ = user.password
        if not self._password_hasher.verify(hash_, input_.password):
            raise UserNotFoundError()

        return VerifyUserOutput.from_user(user)
