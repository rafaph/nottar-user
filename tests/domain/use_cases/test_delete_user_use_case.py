from unittest.mock import AsyncMock

import pytest

from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.use_cases import DeleteUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import DeleteUserInputBuilder

from user.domain.errors import UserNotFoundError
from user.domain.use_cases import DeleteUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(DeleteUserUseCase.__name__)
class TestCreateUserUseCase:
    @pytest.mark.it("Should delete an user")
    async def test_delete_user(self) -> None:
        # given
        user_repository = UserRepositoryBuilder().build()
        delete_mock: AsyncMock = getattr(user_repository, "delete")
        sut = DeleteUserUseCaseBuilder().with_user_repository(user_repository).build()
        input_ = DeleteUserInputBuilder().build()

        # when
        await sut.execute(input_)

        # then
        delete_mock.assert_awaited_once_with(input_.id)

    @pytest.mark.it("Should raise user not found")
    async def test_raise_user_not_found(self) -> None:
        # given
        delete_mock = AsyncMock(side_effect=UserNotFoundError())
        user_repository = UserRepositoryBuilder().with_delete(delete_mock).build()
        sut = DeleteUserUseCaseBuilder().with_user_repository(user_repository).build()
        input_ = DeleteUserInputBuilder().build()

        # when/then
        with pytest.raises(UserNotFoundError):
            await sut.execute(input_)

        # and
        delete_mock.assert_awaited_once_with(input_.id)
