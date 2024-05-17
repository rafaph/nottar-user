from bson import ObjectId

from tests.builders.builder import Builder

from src.domain.models import User
from src.domain.use_cases.outputs import VerifyUserOutput


class VerifyUserOutputBuilder(Builder[VerifyUserOutput]):
    def __init__(self) -> None:
        self._data = {
            "id": str(ObjectId()),
        }
        self._user: User | None = None

    def with_id(self, id_: str) -> "VerifyUserOutputBuilder":
        self._data["id"] = id_
        return self

    def from_user(self, user: User) -> "VerifyUserOutputBuilder":
        self._user = user
        return self

    def build(self) -> VerifyUserOutput:
        if self._user is None:
            return VerifyUserOutput.model_validate(self._data)

        return VerifyUserOutput.from_user(self._user)
