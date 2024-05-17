from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from user.domain.models import User
from user.infra.repositories.mongo.models import UserMongo


class UserDatabase:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self._collection = database[UserMongo.Settings.name]

    async def find_user(self, user_id: str) -> User | None:
        data = await self._collection.find_one({"_id": ObjectId(user_id)})

        if data is None:
            return None

        return User.model_validate(
            {
                "id": str(data.pop("_id")),
                **data,
            }
        )

    async def create_user(
        self,
        user: User,
    ) -> None:
        data = user.model_dump(mode="json")

        await self._collection.insert_one(
            {
                "_id": ObjectId(data.pop("id")),
                **data,
            }
        )
