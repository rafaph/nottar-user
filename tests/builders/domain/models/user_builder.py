from bson import ObjectId
from faker import Faker

from user.domain.models.user import User


class UserBuilder:
    _faker = Faker("en_US")

    def __init__(self) -> None:
        self._id = str(ObjectId())
        self._email = self._faker.email()
        self._first_name = self._faker.first_name()
        self._last_name = self._faker.last_name()
        self._email = self._faker.email()
        self._password = self._faker.password()

    def with_id(self, id_: str) -> "UserBuilder":
        self._id = id_
        return self

    def with_first_name(self, first_name: str) -> "UserBuilder":
        self._first_name = first_name
        return self

    def with_last_name(self, last_name: str) -> "UserBuilder":
        self._last_name = last_name
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def with_password(self, password: str) -> "UserBuilder":
        self._password = password
        return self

    def build(self) -> User:
        return User.model_validate(
            {
                "id": self._id,
                "first_name": self._first_name,
                "last_name": self._last_name,
                "email": self._email,
                "password": self._password,
            }
        )
