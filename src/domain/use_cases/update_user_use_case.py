from injector import inject

from src.common import UseCase
from src.domain.errors import UserEmailInUseError, UserNotFoundError
from src.domain.repositories import UserRepository
from src.domain.services import PasswordHasher
from src.domain.use_cases.inputs import UpdateUserInput
from src.domain.use_cases.outputs import UpdateUserOutput


class UpdateUserUseCase(UseCase[UpdateUserInput, UpdateUserOutput]):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def _user_email_in_use(self, email: str | None, id_: str) -> bool:
        if email is None:
            return False

        try:
            user = await self._user_repository.retrieve_by_email(email)
        except UserNotFoundError:
            return False

        # if the user.id is the same, then it's not in use
        return user.id != id_

    async def execute(self, input_: UpdateUserInput) -> UpdateUserOutput:
        current_user = await self._user_repository.retrieve(input_.id)

        if await self._user_email_in_use(input_.email, input_.id):
            raise UserEmailInUseError()

        updated_user = input_.to_updated_user(current_user, self._password_hasher)

        await self._user_repository.update(updated_user)

        return UpdateUserOutput.from_user(updated_user)
