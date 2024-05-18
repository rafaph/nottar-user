from tests.builders.builder import Builder

from src.infra.controllers.requests import UpdateUserRequest


class UpdateUserRequestBuilder(Builder[UpdateUserRequest]):
    def __init__(self) -> None:
        password = self._faker.password()
        self._data: dict[str, object] = {
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "email": self._faker.email(),
            "password": password,
            "password_confirmation": password,
        }

    def with_first_name(
        self,
        first_name: str | None,
    ) -> "UpdateUserRequestBuilder":
        self._data["first_name"] = first_name
        return self

    def with_last_name(
        self,
        last_name: str | None,
    ) -> "UpdateUserRequestBuilder":
        self._data["last_name"] = last_name
        return self

    def with_email(
        self,
        email: str | None,
    ) -> "UpdateUserRequestBuilder":
        self._data["email"] = email
        return self

    def with_password(
        self,
        password: str | None,
    ) -> "UpdateUserRequestBuilder":
        self._data["password"] = password
        return self

    def with_password_confirmation(
        self,
        password_confirmation: str | None,
    ) -> "UpdateUserRequestBuilder":
        self._data["password_confirmation"] = password_confirmation
        return self

    def build(self) -> UpdateUserRequest:
        return UpdateUserRequest.model_validate(self._data)

    def build_as_dict(self) -> dict[str, object]:
        return self.build().model_dump(mode="json")
