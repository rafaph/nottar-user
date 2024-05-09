import pydash as _

from user.domain.models.user import User
from user.domain.repositories.user_repository import UserRepository
from user.infra.repositories.mongo.models.user_mongo import UserMongo


class MongoUserRespository(UserRepository):
    def create(self, user: User) -> None:
        user_mongo = UserMongo.from_user(user)
        user_mongo.save()

    def update(self, user: User) -> None:
        total_updated = UserMongo.objects.filter(id=user.id).update(
            **_.omit(user.model_dump(mode="json"), "id")
        )

        if total_updated != 1:
            msg = "User not found"
            raise Exception(msg)

    def retrieve(self, user_id: str) -> User:
        user_mongo = UserMongo.objects.get(id=user_id)
        return user_mongo.to_user()

    def delete(self, user_id: str) -> None:
        total_deleted = UserMongo.objects.filter(id=user_id).delete()

        if total_deleted != 1:
            msg = "User not found"
            raise Exception(msg)
