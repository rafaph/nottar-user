from pydantic import BaseModel

from user.domain.models import ObjectIdStr


class DeleteUserInput(BaseModel):
    id: ObjectIdStr
