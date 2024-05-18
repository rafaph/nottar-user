from pydantic import BaseModel, EmailStr, Field

from src.domain.models import ObjectIdStr, User
from src.domain.services import PasswordHasher


class UpdateUserInput(BaseModel):
    id: ObjectIdStr
    first_name: str | None = Field(min_length=2, max_length=100, default=None)
    last_name: str | None = Field(min_length=1, max_length=100, default=None)
    email: EmailStr | None = None
    password: str | None = Field(min_length=1, default=None)

    def to_updated_user(self, old_user: User, password_hasher: PasswordHasher) -> User:
        return User(
            id=self.id,
            first_name=self.first_name or old_user.first_name,
            last_name=self.last_name or old_user.last_name,
            email=self.email or old_user.email,
            password=self.password
            and password_hasher.hash(self.password)
            or old_user.password,
        )
