from typing import Annotated, TypeAlias

from bson import ObjectId as _ObjectId
from pydantic import AfterValidator, StringConstraints, WithJsonSchema


def _after_validator(value: str) -> str:
    if not _ObjectId.is_valid(value):
        msg = "input string should be a valid ObjectId"
        raise ValueError(msg)
    return value


ObjectIdStr: TypeAlias = Annotated[
    str,
    StringConstraints(
        strict=True,
        pattern=r"^[0-9a-z]{24}$",
    ),
    AfterValidator(_after_validator),
    WithJsonSchema(
        {
            "type": "string",
            "example": "66451b4ad5e4fadf9f6a33f4",
        },
    ),
]
