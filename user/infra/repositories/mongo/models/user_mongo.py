from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId

from user.domain.models import User


class UserMongo(Document):
    first_name: str
    last_name: str
    email: Annotated[str, Indexed(unique=True)]
    password: str

    class Settings:
        name = "users"

    @staticmethod
    def from_domain(user: User) -> "UserMongo":
        return UserMongo(
            id=PydanticObjectId(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
        )

    def to_domain(self) -> User:
        return User(
            id=str(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )
