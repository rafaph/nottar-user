import pytest
from assertpy import assert_that
from faker import Faker
from fastapi import status

from tests.builders.domain.models import UserBuilder
from tests.helpers import ServerTest

from user.infra.controllers import DeleteUserController


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(DeleteUserController.__name__)
class TestDeleteUserController:
    @pytest.mark.it(f"Should return {status.HTTP_204_NO_CONTENT}")
    async def test_user_deleted(self) -> None:
        async with ServerTest() as (user_client, user_database):
            # given
            user = UserBuilder().build()
            await user_database.create_user(user)
            user_id = user.id

            # when
            response = await user_client.delete(user_id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_204_NO_CONTENT,
            )

            # and
            user_from_db = await user_database.find_user(user_id)
            assert_that(user_from_db).is_none()

    @pytest.mark.it(f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY}")
    async def test_invalid_user_id(self, faker: Faker) -> None:
        async with ServerTest() as (user_client, _):
            # given
            user_id = faker.currency_symbol()

            # when
            response = await user_client.delete(user_id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @pytest.mark.it(f"Should return {status.HTTP_404_NOT_FOUND}")
    async def test_user_not_found(self) -> None:
        async with ServerTest() as (user_client, _):
            # given
            user = UserBuilder().build()

            # when
            response = await user_client.delete(user.id)

            # then
            assert_that(response.status_code).is_equal_to(
                status.HTTP_404_NOT_FOUND,
            )

            # and
            data: dict[str, str] = response.json()
            assert_that(data).contains_key("detail")
            assert_that(data["detail"]).is_equal_to("User not found")
