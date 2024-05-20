from fastapi import APIRouter, status

from src.common import Controller


class HealthzController(Controller):
    def _healthz(self) -> None:
        pass

    def register(self, router: APIRouter) -> None:
        router.add_api_route(
            "/healthz",
            self._healthz,
            methods=["GET"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
