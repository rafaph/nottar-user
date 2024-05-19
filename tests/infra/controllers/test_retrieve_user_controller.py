import pytest
from assertpy import assert_that
from faker import Faker
from fastapi import status

from tests.builders.domain.models import UserBuilder
from tests.helpers import ServerTest

from src.infra.controllers import RetrieveUserController


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(RetrieveUserController.__name__)
class TestRetrieveUserController:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_retrieve_user(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            await user_database.create_user(user)

            # when
            response = await user_client.retrieve(user.id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_200_OK,
            )

            # and
            response_body = response.json()
            fields = [
                "id",
                "first_name",
                "last_name",
                "email",
            ]
            for field in fields:
                assert_that(response_body).contains_key(field)
                assert_that(response_body[field]).is_equal_to(getattr(user, field))

    @pytest.mark.it(f"Should return {status.HTTP_404_NOT_FOUND} NOT_FOUND")
    async def test_raise_user_not_found(self) -> None:
        async with ServerTest() as (user_client, _):
            # given
            user = UserBuilder().build()

            # when
            response = await user_client.retrieve(user.id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_404_NOT_FOUND,
            )

    @pytest.mark.it(
        f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY} UNPROCESSABLE_ENTITY"
    )
    async def test_unprocessable_entity(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, _):
            # given
            user_id = str(faker.uuid4())

            # when
            response = await user_client.retrieve(user_id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
