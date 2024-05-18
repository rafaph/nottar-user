from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from injector import inject

from src.common import Controller
from src.domain.errors import UserEmailInUseError, UserNotFoundError
from src.domain.models import ObjectIdStr
from src.domain.use_cases import UpdateUserUseCase
from src.infra.controllers.requests import UpdateUserRequest
from src.infra.controllers.responses import ErrorResponse, UpdateUserResponse


class UpdateUserController(Controller):
    @inject
    def __init__(self, use_case: UpdateUserUseCase) -> None:
        self._use_case = use_case

    async def _update_user(
        self,
        user_id: Annotated[ObjectIdStr, Path()],
        request: UpdateUserRequest,
    ) -> UpdateUserResponse:
        try:
            output = await self._use_case.execute(request.to_domain(user_id))

            return UpdateUserResponse.from_domain(output)
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            ) from e
        except UserEmailInUseError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e

    def register(self, router: APIRouter) -> None:
        router.patch(
            "/{user_id}",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "User updated successfully",
                    "model": UpdateUserResponse,
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": (
                        "The provided user id does not have an associated user"
                    ),
                    "model": ErrorResponse[str],
                },
                status.HTTP_409_CONFLICT: {
                    "description": "The provided email is already in use",
                    "model": ErrorResponse[str],
                },
            },
        )(self._update_user)
