from unittest.mock import MagicMock

import argon2
import pytest
from assertpy import assert_that
from faker import Faker

from tests.builders.external import (
    Argon2PasswordHasherBuilder,
)

from user.domain.errors import HashingError
from user.infra.services import Argon2PasswordHasher


@pytest.mark.describe(Argon2PasswordHasher.__name__)
class TestArgon2PasswordHasher:
    _faker = Faker("en_US")

    @pytest.mark.it("Should verify return true if hash and password match")
    def test_verify_true(self) -> None:
        # given
        argon2_password_hasher = Argon2PasswordHasherBuilder().build()
        verify_mock: MagicMock = getattr(argon2_password_hasher, "verify")
        sut = Argon2PasswordHasher(argon2_password_hasher)
        hash_ = str(self._faker.sha256())
        password = self._faker.password()

        # when
        result = sut.verify(hash_, password)

        # then
        assert_that(result).is_true()
        verify_mock.assert_called_once_with(hash_, password)

    @pytest.mark.parametrize(
        "side_effect",
        [
            [argon2.exceptions.InvalidHashError()],
            [argon2.exceptions.VerificationError()],
            [argon2.exceptions.VerifyMismatchError()],
        ],
        ids=["InvalidHashError", "VerificationError", "VerifyMismatchError"],
    )
    @pytest.mark.it("Should verify return false if argon2.verify raise")
    def test_verify_false(self, side_effect: Exception) -> None:
        # given
        verify_mock = MagicMock(side_effect=side_effect)
        argon2_password_hasher = (
            Argon2PasswordHasherBuilder().with_verify(verify_mock).build()
        )
        sut = Argon2PasswordHasher(argon2_password_hasher)
        hash_ = str(self._faker.sha256())
        password = self._faker.password()

        # when
        result = sut.verify(hash_, password)

        # then
        assert_that(result).is_false()
        verify_mock.assert_called_once_with(hash_, password)

    @pytest.mark.it("Should hash return the hashed password")
    def test_hash_success(self) -> None:
        # given
        argon2_password_hasher = Argon2PasswordHasherBuilder().build()
        hash_mock: MagicMock = getattr(argon2_password_hasher, "hash")
        sut = Argon2PasswordHasher(argon2_password_hasher)
        password = self._faker.password()

        # when
        result = sut.hash(password)

        # then
        assert_that(result).is_equal_to(hash_mock.return_value)
        hash_mock.assert_called_once_with(password)

    @pytest.mark.it("Should hash raise a HashingError if hash fails")
    def test_hash_failure(self) -> None:
        # given
        hash_mock = MagicMock(side_effect=argon2.exceptions.HashingError())
        argon2_password_hasher = (
            Argon2PasswordHasherBuilder().with_hash(hash_mock).build()
        )
        sut = Argon2PasswordHasher(argon2_password_hasher)
        password = self._faker.password()

        # when/then
        assert_that(sut.hash).raises(HashingError).when_called_with(password)
        hash_mock.assert_called_once_with(password)

    @pytest.mark.it(
        "Should needs_rehash should return the result of check_needs_rehash"
    )
    def test_needs_rehash(self) -> None:
        # given
        argon2_password_hasher = Argon2PasswordHasherBuilder().build()
        check_needs_rehash_mock: MagicMock = getattr(
            argon2_password_hasher, "check_needs_rehash"
        )
        sut = Argon2PasswordHasher(argon2_password_hasher)
        hash_ = str(self._faker.sha256())

        # when
        result = sut.needs_rehash(hash_)

        # then
        assert_that(result).is_equal_to(check_needs_rehash_mock.return_value)
        check_needs_rehash_mock.assert_called_once_with(hash_)
