from unittest.mock import AsyncMock

import pytest
from assertpy import assert_that

from tests.builders.domain.models import UserBuilder
from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.use_cases import RetrieveUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import RetrieveUserInputBuilder

from src.domain.errors.user_not_found_error import UserNotFoundError
from src.domain.use_cases import RetrieveUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(RetrieveUserUseCase.__name__)
class TestRetrieveUserUseCase:
    @pytest.mark.it("Should retrieve an user")
    async def test_retrieve_user(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_mock = AsyncMock(return_value=user)
        user_repository = UserRepositoryBuilder().with_retrieve(retrieve_mock).build()

        # and
        sut = RetrieveUserUseCaseBuilder().with_user_repository(user_repository).build()

        # and
        input_ = RetrieveUserInputBuilder().with_id(user.id).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(input_.id)
        assert_that(output.first_name).is_equal_to(user.first_name)
        assert_that(output.last_name).is_equal_to(user.last_name)
        assert_that(output.email).is_equal_to(user.email)

        # and
        retrieve_mock.assert_awaited_once_with(user.id)

    @pytest.mark.it("Should raise user not found")
    async def test_raise_user_not_found(self) -> None:
        # given
        retrieve_mock = AsyncMock(side_effect=UserNotFoundError())
        user_repository = UserRepositoryBuilder().with_retrieve(retrieve_mock).build()

        # and
        sut = RetrieveUserUseCaseBuilder().with_user_repository(user_repository).build()

        # and
        input_ = RetrieveUserInputBuilder().build()

        # when/then
        with pytest.raises(UserNotFoundError):
            await sut.execute(input_)

        # and
        retrieve_mock.assert_awaited_once_with(input_.id)
