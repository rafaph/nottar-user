from pydantic import BaseModel, EmailStr

from src.domain.models import User


class RetrieveUserOutput(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr

    @staticmethod
    def from_user(user: User) -> "RetrieveUserOutput":
        return RetrieveUserOutput(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
