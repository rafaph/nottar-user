import argon2
import pytest
from assertpy import assert_that
from faker import Faker
from fastapi import status

from tests.builders.domain.models import UserBuilder
from tests.helpers import ServerTest

from user.infra.controllers import VerifyUserController
from user.infra.services import Argon2PasswordHasher


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(VerifyUserController.__name__)
class TestVerifyUserController:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_verify_user(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            password_hasher = Argon2PasswordHasher(argon2.PasswordHasher())
            raw_password = user.password
            user.password = password_hasher.hash(raw_password)
            await user_database.create_user(user)

            # when
            response = await user_client.verify(
                {
                    "email": user.email,
                    "password": raw_password,
                }
            )

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_200_OK,
            )

            # and
            response_body = response.json()
            assert_that(response_body).contains_key("id")
            assert_that(response_body["id"]).is_equal_to(user.id)

    @pytest.mark.it(
        f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY} " "UNPROCESSABLE_ENTITY"
    )
    async def test_invalid_email(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, _):
            # given/when
            response = await user_client.verify(
                {
                    "email": faker.name(),
                    "password": faker.password(),
                }
            )

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @pytest.mark.it(f"Should return {status.HTTP_401_UNAUTHORIZED} UNAUTHORIZED")
    async def test_invalid_credentials(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            password_hasher = Argon2PasswordHasher(argon2.PasswordHasher())
            user.password = password_hasher.hash(user.password)
            await user_database.create_user(user)

            # when
            response = await user_client.verify(
                {
                    "email": user.email,
                    "password": faker.password(),
                }
            )

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_401_UNAUTHORIZED,
            )
