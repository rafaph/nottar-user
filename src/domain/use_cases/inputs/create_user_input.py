from bson import ObjectId

from src.domain.models import BaseUser, User
from src.domain.services import PasswordHasher


class CreateUserInput(BaseUser):
    def to_user(self, password_hasher: PasswordHasher) -> User:
        return User(
            id=str(ObjectId()),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=password_hasher.hash(self.password),
        )
