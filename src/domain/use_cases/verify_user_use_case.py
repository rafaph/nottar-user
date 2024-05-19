from injector import inject

from src.common import UseCase
from src.domain.errors import UserNotFoundError
from src.domain.repositories import UserRepository
from src.domain.services import PasswordHasher
from src.domain.use_cases.inputs import VerifyUserInput
from src.domain.use_cases.outputs import VerifyUserOutput


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

        if self._password_hasher.needs_rehash(hash_):
            user.password = self._password_hasher.hash(input_.password)
            await self._user_repository.update(user)

        return VerifyUserOutput.from_user(user)
