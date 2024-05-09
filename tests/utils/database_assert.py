# mypy: ignore-errors

from typing import Any

from pymongo import MongoClient
from pymongo.results import InsertOneResult


class DatabaseAssert:
    def __init__(self, client: MongoClient, database: str) -> None:
        self._client = client
        self._database = client[database]

    def find_one(self, collection: str, query: dict[str, Any]) -> dict[str, Any] | None:
        return self._database[collection].find_one(query)

    def create(self, collection: str, data: dict[str, Any]) -> InsertOneResult:
        return self._database[collection].insert_one(data)
