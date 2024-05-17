from injector import inject

from src.common import UseCase
from src.domain.repositories import UserRepository
from src.domain.use_cases.inputs import DeleteUserInput


class DeleteUserUseCase(UseCase[DeleteUserInput, None]):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    async def execute(self, input_: DeleteUserInput) -> None:
        await self._user_repository.delete(input_.id)
