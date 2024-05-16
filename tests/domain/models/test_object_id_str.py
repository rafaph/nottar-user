import pytest
from assertpy import assert_that
from bson import ObjectId
from faker import Faker
from pydantic import TypeAdapter, ValidationError

from user.domain.models import ObjectIdStr


@pytest.mark.describe("ObjectIdStr")
class TestObjectIdStr:
    _type_adapter = TypeAdapter(ObjectIdStr)
    _faker = Faker("en_US")

    @pytest.mark.it("Should be strictally a string")
    def test_strict(self) -> None:
        # given
        value = self._faker.random_int()

        # when/then
        with pytest.raises(ValidationError, match="type=string_type"):
            self._type_adapter.validate_json(str(value))

        # and
        with pytest.raises(ValidationError, match="type=string_type"):
            self._type_adapter.validate_python(value)

    @pytest.mark.it("Should match the pattern")
    def test_pattern(self) -> None:
        # given
        value = self._faker.random_int()

        # when/then
        with pytest.raises(ValidationError, match="type=string_pattern_mismatch"):
            self._type_adapter.validate_json(f'"{value}"')

        # and
        with pytest.raises(ValidationError, match="type=string_pattern_mismatch"):
            self._type_adapter.validate_python(str(value))

    @pytest.mark.it("Should be an ObjectId")
    def test_object_id(self) -> None:
        # given
        value = "g" * 24

        # when/then
        with pytest.raises(ValidationError, match="type=value_error"):
            self._type_adapter.validate_json(f'"{value}"')

        # and
        with pytest.raises(ValidationError, match="type=value_error"):
            self._type_adapter.validate_python(value)

    @pytest.mark.it("Should be valid")
    def test_valid_object_id(self) -> None:
        # given
        value = str(ObjectId())

        # when/then
        self._type_adapter.validate_json(f'"{value}"')
        self._type_adapter.validate_python(value)

    @pytest.mark.it("Should have valid json schema")
    def test_json_schema(self) -> None:
        # given/when
        schema = self._type_adapter.json_schema()

        # then
        assert_that(schema).is_instance_of(dict)

        # and
        assert_that(schema).contains_key("type")
        assert_that(schema["type"]).is_equal_to("string")

        # and
        assert_that(schema).contains_key("example")
        assert_that(ObjectId.is_valid(schema["example"])).is_true()
