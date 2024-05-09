from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=1)
