from injector import inject

from src.common import UseCase
from src.domain.repositories import UserRepository
from src.domain.use_cases.inputs import RetrieveUserInput
from src.domain.use_cases.outputs import RetrieveUserOutput


class RetrieveUserUseCase(UseCase[RetrieveUserInput, RetrieveUserOutput]):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    async def execute(self, input_: RetrieveUserInput) -> RetrieveUserOutput:
        user = await self._user_repository.retrieve(input_.id)

        return RetrieveUserOutput.from_user(user)
