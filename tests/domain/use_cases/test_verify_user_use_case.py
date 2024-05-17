from unittest.mock import ANY, AsyncMock, MagicMock

import pytest
from assertpy import assert_that

from tests.builders.domain.services import PasswordHasherBuilder
from tests.builders.domain.use_cases import VerifyUserUseCaseBuilder
from tests.builders.domain.use_cases.inputs import VerifyUserInputBuilder
from user.domain.errors import UserNotFoundError
from user.domain.models import User
from user.domain.repositories import UserRepository
from user.domain.services import PasswordHasher
from user.domain.use_cases import VerifyUserUseCase


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(VerifyUserUseCase.__name__)
class TestVerifyUserUseCase:
    @pytest.mark.it("Should verify an user")
    async def test_verify_user(self) -> None:
        # given
        sut = VerifyUserUseCaseBuilder().build()
        user_repository: UserRepository = getattr(sut, "_user_repository")
        password_hasher: PasswordHasher = getattr(sut, "_password_hasher")
        retrieve_by_email_mock: AsyncMock = getattr(
            user_repository,
            "retrieve_by_email",
        )
        verify_mock: MagicMock = getattr(password_hasher, "verify")
        user: User = retrieve_by_email_mock.return_value
        input_ = VerifyUserInputBuilder().from_user(user).build()

        # when
        output = await sut.execute(input_)

        # then
        assert_that(output.id).is_equal_to(user.id)
        retrieve_by_email_mock.assert_awaited_once_with(input_.email)
        verify_mock.assert_called_once_with(user.password, input_.password)

    @pytest.mark.it("Should raise user not found if password is not correct")
    async def test_raise_user_not_found(self) -> None:
        # given
        verify_mock = MagicMock(return_value=False)
        password_hasher = PasswordHasherBuilder().with_verify(verify_mock).build()
        sut = VerifyUserUseCaseBuilder().with_password_hasher(password_hasher).build()
        input_ = VerifyUserInputBuilder().build()

        # when/then
        with pytest.raises(UserNotFoundError):
            await sut.execute(input_)

        # and
        verify_mock.assert_called_once_with(ANY, input_.password)
