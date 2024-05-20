from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status
from injector import inject

from src.common import Controller
from src.domain.errors import UserNotFoundError
from src.domain.models import ObjectIdStr
from src.domain.use_cases import DeleteUserUseCase
from src.domain.use_cases.inputs import DeleteUserInput
from src.infra.controllers.responses import ErrorResponse


class DeleteUserController(Controller):
    @inject
    def __init__(self, use_case: DeleteUserUseCase) -> None:
        self._use_case = use_case

    async def _delete_user(
        self,
        user_id: Annotated[ObjectIdStr, Path()],
    ) -> None:
        input_ = DeleteUserInput(id=user_id)

        try:
            await self._use_case.execute(input_)
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            ) from e

    def register(self, router: APIRouter) -> None:
        router.add_api_route(
            "/{user_id}",
            self._delete_user,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "description": (
                        "The provided user id does not have an associated user"
                    ),
                    "model": ErrorResponse[str],
                },
                status.HTTP_204_NO_CONTENT: {
                    "description": "User deleted successfully",
                },
            },
        )
