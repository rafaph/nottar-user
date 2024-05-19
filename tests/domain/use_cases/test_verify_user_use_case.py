from unittest.mock import AsyncMock, MagicMock

import pytest
from assertpy import assert_that
from faker import Faker

from tests.builders.domain.models import UserBuilder
from tests.builders.domain.repositories import UserRepositoryBuilder
from tests.builders.domain.services import PasswordHasherBuilder
from tests.builders.domain.use_cases import VerifyUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import VerifyUserInputBuilder

from src.domain.errors import UserNotFoundError
from src.domain.use_cases import VerifyUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(VerifyUserUseCase.__name__)
class TestVerifyUserUseCase:
    @pytest.mark.it("Should verify an user")
    async def test_verify_user(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_by_email_mock = AsyncMock(return_value=user)
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        verify_mock = MagicMock(return_value=True)
        needs_rehash_mock = MagicMock(return_value=False)
        password_hasher = (
            PasswordHasherBuilder()
            .with_verify(verify_mock)
            .with_needs_rehash(needs_rehash_mock)
            .build()
        )

        # and
        sut = (
            VerifyUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )
        input_ = VerifyUserInputBuilder().with_email(user.email).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)

        # and
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)
        verify_mock.assert_called_once_with(user.password, input_.password)
        needs_rehash_mock.assert_called_once_with(user.password)

    @pytest.mark.it("Should raise UserNotFoundError when user is not found")
    async def test_should_raise_user_not_found(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_by_email_mock = AsyncMock(side_effect=UserNotFoundError())
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        sut = VerifyUserUseCaseBuilder().with_user_repository(user_repository).build()
        input_ = VerifyUserInputBuilder().with_email(user.email).build()

        # when
        with pytest.raises(UserNotFoundError):
            await sut.execute(input_)

        # then
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)

    @pytest.mark.it("Should raise UserNotFoundError when input password is not correct")
    async def test_should_raise_user_not_found_password_not_correct(self) -> None:
        # given
        user = UserBuilder().build()
        retrieve_by_email_mock = AsyncMock(return_value=user)
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve_by_email(retrieve_by_email_mock)
            .build()
        )

        # and
        verify_mock = MagicMock(return_value=False)
        password_hasher = PasswordHasherBuilder().with_verify(verify_mock).build()

        # and
        sut = (
            VerifyUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )
        input_ = VerifyUserInputBuilder().with_email(user.email).build()

        # when
        with pytest.raises(UserNotFoundError):
            await sut.execute(input_)

        # then
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)
        verify_mock.assert_called_once_with(user.password, input_.password)

    @pytest.mark.it("Should rehash a password if it needs to be rehashed")
    async def test_rehash_password(self, faker: Faker) -> None:
        # given
        user = UserBuilder().build()
        old_password_hash = user.password
        retrieve_by_email_mock = AsyncMock(return_value=user)
        update_mock = AsyncMock(return_value=None)
        user_repository = (
            UserRepositoryBuilder()
            .with_retrieve_by_email(retrieve_by_email_mock)
            .with_update(update_mock)
            .build()
        )

        # and
        verify_mock = MagicMock(return_value=True)
        needs_rehash_mock = MagicMock(return_value=True)
        new_password_hash = str(faker.sha256())
        hash_mock = MagicMock(return_value=new_password_hash)
        password_hasher = (
            PasswordHasherBuilder()
            .with_verify(verify_mock)
            .with_needs_rehash(needs_rehash_mock)
            .with_hash(hash_mock)
            .build()
        )

        # and
        sut = (
            VerifyUserUseCaseBuilder()
            .with_user_repository(user_repository)
            .with_password_hasher(password_hasher)
            .build()
        )
        input_ = VerifyUserInputBuilder().with_email(user.email).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)

        # and
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)
        verify_mock.assert_called_once_with(old_password_hash, input_.password)
        needs_rehash_mock.assert_called_once_with(old_password_hash)
        hash_mock.assert_called_once_with(input_.password)
        update_mock.assert_awaited_once_with(user)
