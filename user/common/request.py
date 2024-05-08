from dataclasses import dataclass
from typing import Generic, TypeVar

Body = TypeVar("Body")


@dataclass
class Request(Generic[Body]):
    body: Body
