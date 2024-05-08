from dataclasses import dataclass
from http import HTTPStatus
from typing import Generic, TypeVar

Body = TypeVar("Body")


@dataclass
class Response(Generic[Body]):
    status: HTTPStatus
    body: Body
