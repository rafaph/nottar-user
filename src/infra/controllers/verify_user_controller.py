from fastapi import APIRouter, HTTPException, status
from injector import inject

from src.common import Controller
from src.domain.errors import UserNotFoundError
from src.domain.use_cases import VerifyUserUseCase
from src.infra.controllers.requests import VerifyUserRequest
from src.infra.controllers.responses import ErrorResponse, VerifyUserResponse


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
        router.add_api_route(
            "/verify",
            self._verify_user,
            methods=["POST"],
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
        )
