from tests.builders.builder import Builder
from user.domain.models import User
from user.domain.use_cases.inputs import VerifyUserInput


class VerifyUserInputBuilder(Builder[VerifyUserInput]):
    def __init__(self) -> None:
        self._data = {
            "email": self._faker.email(),
            "password": self._faker.password(),
        }
        self._user: User | None = None

    def with_email(self, email: str) -> "VerifyUserInputBuilder":
        self._data["email"] = email
        return self

    def with_password(self, password: str) -> "VerifyUserInputBuilder":
        self._data["password"] = password
        return self

    def from_user(self, user: User) -> "VerifyUserInputBuilder":
        self._user = user
        return self

    def build(self) -> VerifyUserInput:
        if self._user is not None:
            self._data.update(
                {
                    "email": self._user.email,
                    "password": self._user.password,
                }
            )

        return VerifyUserInput.model_validate(self._data)
