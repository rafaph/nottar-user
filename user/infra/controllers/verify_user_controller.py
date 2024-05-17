from fastapi import APIRouter, HTTPException, status
from injector import inject

from user.common import Controller
from user.domain.errors import UserNotFoundError
from user.domain.use_cases import VerifyUserUseCase
from user.infra.controllers.requests import VerifyUserRequest
from user.infra.controllers.responses import ErrorResponse, VerifyUserResponse


class VerifyUserController(Controller):
    @inject
    def __init__(self, use_case: VerifyUserUseCase) -> None:
        self._use_case = use_case

    async def _verify_user(self, request: VerifyUserRequest) -> VerifyUserResponse:
        try:
            output = await self._use_case.execute(request.to_domain())
            return VerifyUserResponse.from_domain(output)
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or incorrect password",
            ) from e

    def register(self, router: APIRouter) -> None:
        router.post(
            "/verify",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "User not found or incorrect password",
                    "model": ErrorResponse[str],
                },
                status.HTTP_200_OK: {
                    "description": "User verified successfully",
                    "model": VerifyUserResponse,
                },
            },
        )(self._verify_user)
