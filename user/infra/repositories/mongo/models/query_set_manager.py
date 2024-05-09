import types
from typing import Generic, TypeVar

from mongoengine import Document, QuerySet


def no_op(self: object, _x: object) -> object:
    return self


QuerySet.__class_getitem__ = types.MethodType(no_op, QuerySet)

U = TypeVar("U", bound=Document)


class QuerySetManager(Generic[U]):
    def __get__(self, instance: object, cls: type[U]) -> QuerySet[U]:
        return QuerySet(cls, cls._get_collection())
