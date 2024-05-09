from mongoengine import Document, fields

from user.domain.models.user import User
from user.infra.repositories.mongo.models.query_set_manager import QuerySetManager


class UserMongo(Document):
    id = fields.ObjectIdField(primary_key=True, required=True)
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)
    email = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)

    objects = QuerySetManager["UserMongo"]()
    meta = {
        "collection": "users",
        "indexes": ["email"],
        "id_field": "id",
    }

    def to_user(self) -> User:
        return User.model_validate(
            {
                "id": str(self.id),
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "password": self.password,
            }
        )

    @staticmethod
    def from_user(user: User) -> "UserMongo":
        return UserMongo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
        )
