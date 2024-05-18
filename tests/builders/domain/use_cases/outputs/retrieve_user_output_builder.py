from bson import ObjectId

from tests.builders.builder import Builder

from src.domain.models import User
from src.domain.use_cases.outputs import RetrieveUserOutput


class RetrieveUserOutputBuilder(Builder[RetrieveUserOutput]):
    def __init__(self) -> None:
        self._data = {
            "id": str(ObjectId()),
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "email": self._faker.email(),
        }
        self._user: User | None = None

    def with_id(self, id_: str) -> "RetrieveUserOutputBuilder":
        self._data["id"] = id_
        return self

    def with_first_name(self, first_name: str) -> "RetrieveUserOutputBuilder":
        self._data["first_name"] = first_name
        return self

    def with_last_name(self, last_name: str) -> "RetrieveUserOutputBuilder":
        self._data["last_name"] = last_name
        return self

    def with_email(self, email: str) -> "RetrieveUserOutputBuilder":
        self._data["email"] = email
        return self

    def from_user(self, user: User) -> "RetrieveUserOutputBuilder":
        self._user = user
        return self

    def build(self) -> RetrieveUserOutput:
        if self._user is None:
            return RetrieveUserOutput.model_validate(self._data)

        return RetrieveUserOutput.from_user(self._user)
