import pytest
from assertpy import assert_that

from tests.builders.domain.models import UserBuilder
from tests.helpers import DatabaseTest

from user.domain.errors import UserNotFoundError
from user.infra.repositories.mongo import MongoUserRepository


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(MongoUserRepository.__name__)
class TestMongoUserRepository:
    @pytest.mark.it("Should create the user")
    async def test_should_create_user(self) -> None:
        async with DatabaseTest() as db:
            # given
            user = UserBuilder().build()
            sut = MongoUserRepository()

            # when
            await sut.create(user)

            # then
            user_from_db = await db.find_user(user.id)
            assert_that(user_from_db).is_equal_to(user)

    @pytest.mark.it("Should retrieve the user by id")
    async def test_retrieve_user(self) -> None:
        async with DatabaseTest() as db:
            # given
            user = UserBuilder().build()
            await db.create_user(user)
            sut = MongoUserRepository()

            # when
            user_from_db = await sut.retrieve(user.id)

            # then
            assert_that(user_from_db).is_equal_to(user)

    @pytest.mark.it(
        "Should raise UserNotFoundError when trying to retrieve an "
        "user by id that does not exist"
    )
    async def test_retrieve_raise_user_not_found(self) -> None:
        async with DatabaseTest():
            # given
            user = UserBuilder().build()
            sut = MongoUserRepository()

            # when/then
            with pytest.raises(UserNotFoundError):
                await sut.retrieve(user.id)

    @pytest.mark.it("Should retrieve the user by email")
    async def test_retrieve_user_email(self) -> None:
        async with DatabaseTest() as db:
            # given
            user = UserBuilder().build()
            await db.create_user(user)
            sut = MongoUserRepository()

            # when
            user_from_db = await sut.retrieve_by_email(user.email)

            # then
            assert_that(user_from_db).is_equal_to(user)

    @pytest.mark.it(
        "Should raise UserNotFoundError when trying to retrieve an "
        "user by email that does not exist"
    )
    async def test_retrieve_raise_user_email_not_found(self) -> None:
        async with DatabaseTest():
            # given
            user = UserBuilder().build()
            sut = MongoUserRepository()

            # when/then
            with pytest.raises(UserNotFoundError):
                await sut.retrieve_by_email(user.email)

    @pytest.mark.it("Should update the user")
    async def test_update_user(self) -> None:
        async with DatabaseTest() as db:
            # given
            user = UserBuilder().build()
            await db.create_user(user)
            sut = MongoUserRepository()
            user_to_update = UserBuilder().with_id(user.id).build()

            # when
            await sut.update(user_to_update)

            # then
            user_from_db = await db.find_user(user.id)
            assert_that(user_from_db).is_equal_to(user_to_update)

    @pytest.mark.it(
        "Should raise UserNotFoundError when trying to update an "
        "user that does not exist"
    )
    async def test_update_raise_user_not_found(self) -> None:
        async with DatabaseTest():
            # given
            user = UserBuilder().build()
            sut = MongoUserRepository()

            # when/then
            with pytest.raises(UserNotFoundError):
                await sut.update(user)

    @pytest.mark.it("Should delete the user")
    async def test_delete_user(self) -> None:
        async with DatabaseTest() as db:
            # given
            user = UserBuilder().build()
            await db.create_user(user)
            sut = MongoUserRepository()

            # when
            await sut.delete(user.id)

            # then
            user_from_db = await db.find_user(user.id)
            assert_that(user_from_db).is_none()

    @pytest.mark.it(
        "Should raise UserNotFoundError when trying to delete an "
        "user that does not exist"
    )
    async def test_delete_raise_user_not_found(self) -> None:
        async with DatabaseTest():
            # given
            user = UserBuilder().build()
            sut = MongoUserRepository()

            # when/then
            with pytest.raises(UserNotFoundError):
                await sut.delete(user.id)
