from bson import ObjectId

from tests.builders.domain.models.base_user_builder import BaseUserBuilder

from src.domain.models import User


class UserBuilder(BaseUserBuilder[User]):
    def __init__(self) -> None:
        super().__init__()
        self._data["id"] = str(ObjectId())

    def with_id(self, id_: str) -> "UserBuilder":
        self._data["id"] = id_
        return self

    def build(self) -> User:
        return User.model_validate(self._data)
