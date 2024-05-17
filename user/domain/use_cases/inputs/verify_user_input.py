from pydantic import BaseModel, EmailStr, Field


class VerifyUserInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
