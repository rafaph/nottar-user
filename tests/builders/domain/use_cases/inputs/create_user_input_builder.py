from tests.builders.domain.models.base_user_builder import BaseUserBuilder
from user.domain.use_cases.inputs import CreateUserInput


class CreateUserInputBuilder(BaseUserBuilder[CreateUserInput]):
    def build(self) -> CreateUserInput:
        return CreateUserInput.model_validate(self._data)
