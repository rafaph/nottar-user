from pydantic import BaseModel

from src.domain.models import ObjectIdStr


class DeleteUserInput(BaseModel):
    id: ObjectIdStr
