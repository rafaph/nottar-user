from types import TracebackType

from bson import ObjectId
from mongoengine.connection import connect, disconnect
from pymongo import MongoClient

from tests.utils.database_assert import DatabaseAssert


class DatabaseTest:
    _client: MongoClient
    db_assert: DatabaseAssert

    def __init__(self) -> None:
        self.database_name = str(ObjectId())

    def __enter__(self) -> "DatabaseTest":
        self._client = connect(
            host="mongodb://admin:admin@127.0.0.1:27017",
            db=self.database_name,
            uuidRepresentation="pythonLegacy",
        )
        self.db_assert = DatabaseAssert(self._client, self.database_name)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._client.drop_database(self.database_name)  # type: ignore
        disconnect()
