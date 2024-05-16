from pydantic import BaseModel, EmailStr, Field

from user.domain.models.object_id_str import ObjectIdStr


class BaseUser(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=1)


class User(BaseUser):
    id: ObjectIdStr
