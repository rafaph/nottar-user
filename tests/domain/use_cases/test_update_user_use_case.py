from unittest.mock import AsyncMock

import pytest
from assertpy import assert_that

from tests.builders.domain.models import UserBuilder
from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.services import PasswordHasherBuilder
from tests.builders.domain.use_cases import UpdateUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import UpdateUserInputBuilder

from src.domain.errors import UserEmailInUseError, UserNotFoundError
from src.domain.use_cases import UpdateUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(UpdateUserUseCase.__name__)
class TestUpdateUserUseCase:
    @pytest.mark.it("Should update an user completely")
    async def test_update_user_completely(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_mock = AsyncMock(return_value=user)
        retrieve_by_email_mock = AsyncMock(side_effect=UserNotFoundError())
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve(retrieve_mock)
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        password_hasher = PasswordHasherBuilder().build()

        # and
        sut = (
            UpdateUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )

        # and
        input_ = UpdateUserInputBuilder().with_id(user.id).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)
        assert_that(output.first_name).is_equal_to(input_.first_name)
        assert_that(output.last_name).is_equal_to(input_.last_name)
        assert_that(output.email).is_equal_to(input_.email)

        # and
        retrieve_mock.assert_awaited_once_with(input_.id)
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)

    @pytest.mark.it("Should update an user without email")
    async def test_update_user_without_email(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_mock = AsyncMock(return_value=user)
        user_repository = UserRepositoryBuilder().with_retrieve(retrieve_mock).build()

        # and
        password_hasher = PasswordHasherBuilder().build()

        # and
        sut = (
            UpdateUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )

        # and
        input_ = UpdateUserInputBuilder().with_id(user.id).with_email(None).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)
        assert_that(output.first_name).is_equal_to(input_.first_name)
        assert_that(output.last_name).is_equal_to(input_.last_name)
        assert_that(output.email).is_equal_to(user.email)

        # and
        retrieve_mock.assert_awaited_once_with(input_.id)

    @pytest.mark.it("Should update an user with the same email")
    async def test_update_user_with_same_email(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_mock = AsyncMock(return_value=user)
        retrieve_by_email_mock = AsyncMock(return_value=user)
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve(retrieve_mock)
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        password_hasher = PasswordHasherBuilder().build()

        # and
        sut = (
            UpdateUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )

        # and
        input_ = (
            UpdateUserInputBuilder().with_id(user.id).with_email(user.email).build()
        )

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)
        assert_that(output.first_name).is_equal_to(input_.first_name)
        assert_that(output.last_name).is_equal_to(input_.last_name)
        assert_that(output.email).is_equal_to(user.email)

        # and
        retrieve_mock.assert_awaited_once_with(input_.id)
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)

    @pytest.mark.it(
        "Should raise UserEmailInUseError if email is in use by another user"
    )
    async def test_update_user_raise_email_in_use(self) -> None:
        # given
        user = UserBuilder().build()
        another_user = UserBuilder().build()
        retrieve_mock = AsyncMock(return_value=user)
        retrieve_by_email_mock = AsyncMock(return_value=another_user)
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve(retrieve_mock)
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        password_hasher = PasswordHasherBuilder().build()

        # and
        sut = (
            UpdateUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )

        # and
        input_ = (
            UpdateUserInputBuilder()
            .with_id(user.id)
            .with_email(another_user.email)
            .build()
        )

        # when/then
        with pytest.raises(UserEmailInUseError):
            await sut.execute(input_)

        # and
        retrieve_mock.assert_awaited_once_with(input_.id)
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)
