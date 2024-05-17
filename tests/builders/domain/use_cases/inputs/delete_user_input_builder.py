from bson import ObjectId

from tests.builders.builder import Builder

from user.domain.use_cases.inputs import DeleteUserInput


class DeleteUserInputBuilder(Builder[DeleteUserInput]):
    def __init__(self) -> None:
        self._data = {
            "id": str(ObjectId()),
        }

    def with_id(self, id_: str) -> "DeleteUserInputBuilder":
        self._data["id"] = id_
        return self

    def build(self) -> DeleteUserInput:
        return DeleteUserInput.model_validate(self._data)
