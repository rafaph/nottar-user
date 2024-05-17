import pytest
from assertpy import assert_that
from faker import Faker
from fastapi import status

from tests.builders.domain.models import UserBuilder
from tests.builders.infra.controllers.requests import CreateUserRequestBuilder
from tests.helpers import ServerTest

from user.infra.controllers import CreateUserController


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(CreateUserController.__name__)
class TestCreateUserController:
    @pytest.mark.it(f"Should return {status.HTTP_201_CREATED}")
    async def test_user_created(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            body = CreateUserRequestBuilder().build_as_dict()

            # when
            response = await user_client.create(body)

            # then
            assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

            # and
            response_body = response.json()
            fields = ["id", "first_name", "last_name", "email"]
            assert_that(response_body).contains(*fields)

            # and
            user_from_database = await user_database.find_user(response_body["id"])
            assert_that(user_from_database).is_not_none()

            # and
            for field in fields:
                value_from_response = response_body[field]
                value_from_database = getattr(user_from_database, field)
                assert_that(value_from_response).is_equal_to(value_from_database)

    @pytest.mark.it(f"Should return {status.HTTP_409_CONFLICT}")
    async def test_user_email_in_use(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            body = CreateUserRequestBuilder().build_as_dict()
            user = UserBuilder().with_email(str(body["email"])).build()
            await user_database.create_user(user)

            # when
            response = await user_client.create(body)

            # then
            assert_that(response.status_code).is_equal_to(status.HTTP_409_CONFLICT)

    @pytest.mark.it(f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY}")
    async def test_passwords_do_not_match(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, _):
            # given
            body = CreateUserRequestBuilder().build_as_dict()
            body["password_confirmation"] = faker.password()

            # when
            response = await user_client.create(body)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
