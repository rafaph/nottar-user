from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status
from injector import inject

from user.common import Controller
from user.domain.errors import UserNotFoundError
from user.domain.models import ObjectIdStr
from user.domain.use_cases import DeleteUserUseCase
from user.domain.use_cases.inputs import DeleteUserInput
from user.infra.controllers.responses import ErrorResponse


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
        router.delete(
            "/{user_id}",
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
        )(self._delete_user)
