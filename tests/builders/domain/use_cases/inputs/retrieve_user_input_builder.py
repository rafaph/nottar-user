from bson import ObjectId

from tests.builders.builder import Builder

from src.domain.use_cases.inputs import RetrieveUserInput


class RetrieveUserInputBuilder(Builder[RetrieveUserInput]):
    def __init__(self) -> None:
        self._data = {
            "id": str(ObjectId()),
        }

    def with_id(self, id_: str) -> "RetrieveUserInputBuilder":
        self._data["id"] = id_
        return self

    def build(self) -> RetrieveUserInput:
        return RetrieveUserInput.model_validate(self._data)
