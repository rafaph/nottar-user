import pydash as _
from beanie import PydanticObjectId

from src.domain.errors import UserNotFoundError
from src.domain.models import User
from src.domain.repositories import UserRepository
from src.infra.repositories.mongo.models import UserMongo


class MongoUserRepository(UserRepository):
    async def create(self, user: User) -> None:
        user_mongo = UserMongo.from_domain(user)
        await user_mongo.create()

    async def retrieve(self, user_id: str) -> User:
        user_mongo: UserMongo | None = await UserMongo.get(user_id)

        if user_mongo is None:
            raise UserNotFoundError()

        return user_mongo.to_domain()

    async def retrieve_by_email(self, email: str) -> User:
        user_mongo: UserMongo | None = await UserMongo.find(
            {"email": email}
        ).first_or_none()

        if user_mongo is None:
            raise UserNotFoundError()

        return user_mongo.to_domain()

    async def update(self, user: User) -> None:
        user_ = _.omit(
            user.model_dump(mode="json"),
            "id",
        )
        filter_ = {"_id": PydanticObjectId(user.id)}
        operation = {"$set": user_}

        result = await UserMongo.find_one(filter_).update(operation)

        if result.modified_count != 1:
            raise UserNotFoundError()

    async def delete(self, user_id: str) -> None:
        filter_ = {"_id": PydanticObjectId(user_id)}
        result = await UserMongo.find_one(filter_).delete()

        if result is None or result.deleted_count != 1:
            raise UserNotFoundError()
