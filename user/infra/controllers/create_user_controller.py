from fastapi import APIRouter, HTTPException, status
from injector import inject

from user.common import Controller
from user.domain.errors import UserEmailInUseError
from user.domain.use_cases import CreateUserUseCase
from user.infra.controllers.requests import CreateUserRequest
from user.infra.controllers.responses import CreateUserResponse, ErrorResponse


class CreateUserController(Controller):
    @inject
    def __init__(self, use_case: CreateUserUseCase) -> None:
        self._use_case = use_case

    async def _create_user(self, input_: CreateUserRequest) -> CreateUserResponse:
        try:
            output = await self._use_case.execute(input_.to_domain())
            return CreateUserResponse.from_domain(output)
        except UserEmailInUseError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e

    def register(self, router: APIRouter) -> None:
        router.post(
            "/",
            status_code=status.HTTP_201_CREATED,
            responses={
                status.HTTP_409_CONFLICT: {
                    "description": "The provided email is already in use",
                    "model": ErrorResponse[str],
                },
                status.HTTP_201_CREATED: {
                    "description": "User created successfully",
                    "model": CreateUserResponse,
                },
            },
        )(self._create_user)
