from pydantic import BaseModel, EmailStr

from user.domain.models import User


class CreateUserOutput(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr

    @staticmethod
    def from_user(user: User) -> "CreateUserOutput":
        return CreateUserOutput(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
