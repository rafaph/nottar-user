from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from injector import inject

from src.common import Controller
from src.domain.errors import UserNotFoundError
from src.domain.models import ObjectIdStr
from src.domain.use_cases import RetrieveUserUseCase
from src.domain.use_cases.inputs import RetrieveUserInput
from src.infra.controllers.responses import ErrorResponse, RetrieveUserResponse


class RetrieveUserController(Controller):
    @inject
    def __init__(self, use_case: RetrieveUserUseCase) -> None:
        self._use_case = use_case

    async def _retrieve_user(
        self,
        user_id: Annotated[ObjectIdStr, Path()],
    ) -> RetrieveUserResponse:
        input_ = RetrieveUserInput(id=user_id)

        try:
            output = await self._use_case.execute(input_)

            return RetrieveUserResponse.from_domain(output)
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            ) from e

    def register(self, router: APIRouter) -> None:
        router.add_api_route(
            "/{user_id}",
            self._retrieve_user,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "description": (
                        "The provided user id does not have an associated user"
                    ),
                    "model": ErrorResponse[str],
                },
                status.HTTP_200_OK: {
                    "description": "User retrieved successfully",
                    "model": RetrieveUserResponse,
                },
            },
        )
