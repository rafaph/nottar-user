from pydantic import BaseModel

from src.domain.models import ObjectIdStr


class RetrieveUserInput(BaseModel):
    id: ObjectIdStr
