from bson import ObjectId

from tests.builders.builder import Builder

from src.domain.use_cases.inputs import UpdateUserInput


class UpdateUserInputBuilder(Builder[UpdateUserInput]):
    def __init__(self) -> None:
        self._data: dict[str, str | None] = {
            "id": str(ObjectId()),
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "email": self._faker.email(),
            "password": self._faker.password(),
        }

    def with_id(self, id_: str) -> "UpdateUserInputBuilder":
        self._data["id"] = id_
        return self

    def with_first_name(
        self,
        first_name: str | None = None,
    ) -> "UpdateUserInputBuilder":
        self._data["first_name"] = first_name
        return self

    def with_last_name(
        self,
        last_name: str | None = None,
    ) -> "UpdateUserInputBuilder":
        self._data["last_name"] = last_name
        return self

    def with_email(
        self,
        email: str | None = None,
    ) -> "UpdateUserInputBuilder":
        self._data["email"] = email
        return self

    def with_password(
        self,
        password: str | None = None,
    ) -> "UpdateUserInputBuilder":
        self._data["password"] = password
        return self

    def build(self) -> UpdateUserInput:
        return UpdateUserInput.model_validate(self._data)
