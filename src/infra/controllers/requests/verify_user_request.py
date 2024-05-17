from pydantic import BaseModel, EmailStr, Field

from src.domain.use_cases.inputs import VerifyUserInput


class VerifyUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

    def to_domain(self) -> VerifyUserInput:
        return VerifyUserInput(
            email=self.email,
            password=self.password,
        )
