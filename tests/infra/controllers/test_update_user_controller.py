import pytest
from assertpy import assert_that
from bson import ObjectId
from faker import Faker
from fastapi import status

from tests.builders.domain.models import UserBuilder
from tests.builders.infra.controllers.requests import UpdateUserRequestBuilder
from tests.helpers import ServerTest

from src.infra.controllers import UpdateUserController


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(UpdateUserController.__name__)
class TestUpdateUserController:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_return_ok(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            await user_database.create_user(user)
            body = UpdateUserRequestBuilder().build_as_dict()

            # when
            response = await user_client.update(user.id, body)

            # then
            assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

            # and
            response_body = response.json()
            assert_that(response_body).contains_key("id")
            assert_that(response_body["id"]).is_equal_to(user.id)

            # and
            user_from_database = await user_database.find_user(response_body["id"])
            assert_that(user_from_database).is_not_none()

            # and
            for field in ["first_name", "last_name", "email"]:
                value_from_response = response_body[field]
                value_from_database = getattr(user_from_database, field)
                assert_that(value_from_response).is_equal_to(value_from_database)

    @pytest.mark.it(f"Should return {status.HTTP_404_NOT_FOUND} NOT_FOUND")
    async def test_return_not_found(self) -> None:
        async with ServerTest() as (user_client, _):
            # given
            user = UserBuilder().build()
            body = UpdateUserRequestBuilder().build_as_dict()

            # when
            response = await user_client.update(user.id, body)

            # then
            assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)

    @pytest.mark.it(f"Should return {status.HTTP_409_CONFLICT} CONFLICT")
    async def test_return_conflict(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            another_user = UserBuilder().build()
            await user_database.create_user(user)
            await user_database.create_user(another_user)
            body = (
                UpdateUserRequestBuilder()
                .with_email(another_user.email)
                .build_as_dict()
            )

            # when
            response = await user_client.update(user.id, body)

            # then
            assert_that(response.status_code).is_equal_to(status.HTTP_409_CONFLICT)

    @pytest.mark.it(
        f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY} UNPROCESSABLE_ENTITY"
    )
    async def test_return_unprocessable_entity(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, _):
            # given
            test_cases = [
                (str(faker.uuid4()), {}),
                (
                    str(ObjectId()),
                    {
                        **UpdateUserRequestBuilder().build_as_dict(),
                        "password": None,
                    },
                ),
            ]
            for user_id, body in test_cases:
                # when
                response = await user_client.update(user_id, body)

                # then
                assert_that(response.status_code).is_equal_to(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
