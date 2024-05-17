from unittest.mock import AsyncMock

import pytest
from assertpy import assert_that
from bson import ObjectId

from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.use_cases import CreateUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import CreateUserInputBuilder

from user.domain.errors import UserEmailInUseError, UserNotFoundError
from user.domain.use_cases import CreateUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(CreateUserUseCase.__name__)
class TestCreateUserUseCase:
    @pytest.mark.it("Should return an output")
    async def test_return_an_output(self) -> None:
        # given
        retrieve_by_email_mock = AsyncMock(side_effect=UserNotFoundError())
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )
        input_ = CreateUserInputBuilder().build()
        sut = CreateUserUseCaseBuilder().with_user_repository(user_repository).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(ObjectId.is_valid(output.id)).is_true()
        assert_that(output.first_name).is_equal_to(input_.first_name)
        assert_that(output.last_name).is_equal_to(input_.last_name)
        assert_that(output.email).is_equal_to(input_.email)

    @pytest.mark.it("Should raise UserEmailInUseError when email is already in use")
    async def test_raise_user_email_in_use_error(self) -> None:
        # given
        input_ = CreateUserInputBuilder().build()
        sut = CreateUserUseCaseBuilder().build()

        # when/then
        with pytest.raises(UserEmailInUseError):
            await sut.execute(input_)
