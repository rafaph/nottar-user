from types import TracebackType

from beanie import init_beanie
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from tests.helpers.user_database import UserDatabase

from src.infra.repositories.mongo.models import UserMongo


class DatabaseTest:
    def __init__(self) -> None:
        self._database_name = str(ObjectId())
        self._client: AsyncIOMotorClient | None = None
        self._database: AsyncIOMotorDatabase | None = None

    async def up(self) -> None:
        self._client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
        self._database = self._client[self._database_name]
        await init_beanie(database=self._database, document_models=[UserMongo])

    async def down(self) -> None:
        if self._client is None:
            msg = "client is None, forgot to call up method?"
            raise Exception(msg)

        await self._client.drop_database(self._database_name)

        self._client.close()

    @property
    def user_database(self) -> UserDatabase:
        if self._database is None:
            msg = "database is None, forgot to call up method?"
            raise Exception(msg)

        return UserDatabase(self._database)

    @property
    def database_url(self) -> str:
        return f"mongodb://admin:admin@localhost:27017/{self._database_name}?authSource=admin"

    async def __aenter__(self) -> UserDatabase:
        await self.up()
        return self.user_database

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.down()
