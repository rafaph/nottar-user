from pydantic import BaseModel

from user.domain.models import User


class VerifyUserOutput(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User) -> "VerifyUserOutput":
        return VerifyUserOutput(
            id=user.id,
        )
