import pydash as _
import pytest
from assertpy import assert_that
from bson import ObjectId

from tests.builders.domain.models.user_builder import UserBuilder
from tests.utils.database_test import DatabaseTest
from user.infra.repositories.mongo.mongo_user_repository import MongoUserRespository


@pytest.mark.describe(MongoUserRespository.__name__)
class TestMongoUserRespository:
    @pytest.mark.it("Should create the user")
    def test_should_create_user(self) -> None:
        with DatabaseTest() as dt:
            # given
            user = UserBuilder().build()

            # when
            MongoUserRespository().create(user)

            # then
            user_mongo = dt.db_assert.find_one("users", {"_id": ObjectId(user.id)})
            assert_that(user_mongo).is_not_none()

    @pytest.mark.it("Should retrieve the user by id")
    def test_retrieve_user(self) -> None:
        with DatabaseTest() as dt:
            # given
            user = UserBuilder().build()
            data = user.model_dump(mode="json")
            _id = ObjectId(data.pop("id"))
            dt.db_assert.create("users", {"_id": _id, **data})

            # when
            user_from_db = MongoUserRespository().retrieve(user.id)

            # then
            assert_that(user_from_db).is_equal_to(user)

    @pytest.mark.it("Should update the user")
    def test_update_user(self) -> None:
        with DatabaseTest() as dt:
            # given
            user = UserBuilder().build()
            data = user.model_dump(mode="json")
            _id = ObjectId(data.pop("id"))
            dt.db_assert.create("users", {"_id": _id, **data})
            user_to_update = UserBuilder().with_id(user.id).build()

            # when
            MongoUserRespository().update(user_to_update)

            # then
            user_from_db = dt.db_assert.find_one("users", {"_id": _id})
            assert_that(user_from_db).is_not_none()
            assert_that(
                _.omit(user_from_db, "_id"),
            ).is_equal_to(
                _.omit(user_to_update.model_dump(mode="json"), "id"),
            )

    @pytest.mark.it("Should not update an user if he does not exist")
    def test_not_update_user(self) -> None:
        # given
        user = UserBuilder().build()

        # when/then
        with DatabaseTest(), pytest.raises(Exception, match="User not found"):
            MongoUserRespository().update(user)

    @pytest.mark.it("Should delete the user")
    def test_delete_user(self) -> None:
        with DatabaseTest() as dt:
            # given
            user = UserBuilder().build()
            data = user.model_dump(mode="json")
            _id = ObjectId(data.pop("id"))
            dt.db_assert.create("users", {"_id": _id, **data})

            # when
            MongoUserRespository().delete(user.id)

            # then
            user_from_db = dt.db_assert.find_one("users", {"_id": _id})
            assert_that(user_from_db).is_none()

    @pytest.mark.it("Should not delete an user if he does not exist")
    def test_not_delete_user(self) -> None:
        # given
        user = UserBuilder().build()

        # when/then
        with DatabaseTest(), pytest.raises(Exception, match="User not found"):
            MongoUserRespository().delete(user.id)
