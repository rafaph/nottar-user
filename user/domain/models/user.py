from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseUser(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=1)


class User(BaseUser):
    id: str

    @field_validator("id")
    @classmethod
    def _id_validator(cls, value: str) -> str:
        if not ObjectId.is_valid(value):
            msg = "Invalid id"
            raise ValueError(msg)

        return value
