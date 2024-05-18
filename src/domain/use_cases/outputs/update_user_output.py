from pydantic import BaseModel, EmailStr

from src.domain.models import User


class UpdateUserOutput(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr

    @staticmethod
    def from_user(user: User) -> "UpdateUserOutput":
        return UpdateUserOutput(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
