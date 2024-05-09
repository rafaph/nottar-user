from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from user.common.request import Request
from user.common.response import Response

RequestBody = TypeVar("RequestBody")
ResponseBody = TypeVar("ResponseBody")


class Controller(ABC, Generic[RequestBody, ResponseBody]):
    @property
    @abstractmethod
    def path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        request: Request[RequestBody],
    ) -> Response[ResponseBody]:
        raise NotImplementedError
