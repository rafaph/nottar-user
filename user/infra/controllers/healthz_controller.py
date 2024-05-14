from fastapi import APIRouter, status

from user.common import Controller


class HealthzController(Controller):
    def _healthz(self) -> None:
        pass

    def register(self, router: APIRouter) -> None:
        router.get(
            "/healthz",
            status_code=status.HTTP_204_NO_CONTENT,
        )(self._healthz)