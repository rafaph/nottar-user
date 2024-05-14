from abc import ABC, abstractmethod

from fastapi import APIRouter


class Controller(ABC):
    @abstractmethod
    def register(self, router: APIRouter) -> None:
        raise NotImplementedError  # pragma: no cover
