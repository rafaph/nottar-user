from tests.builders.domain.models.base_user_builder import BaseUserBuilder

from user.infra.controllers.requests import CreateUserRequest


class CreateUserRequestBuilder(BaseUserBuilder[CreateUserRequest]):
    def __init__(self) -> None:
        super().__init__()
        self._data["password_confirmation"] = self._data["password"]

    def with_password_confirmation(
        self,
        password_confirmation: str,
    ) -> "CreateUserRequestBuilder":
        self._data["password_confirmation"] = password_confirmation
        return self

    def build(self) -> CreateUserRequest:
        return CreateUserRequest.model_validate(self._data)

    def build_as_dict(self) -> dict[str, object]:
        return self.build().model_dump(mode="json")
