import pytest
from pydantic import ValidationError

from tests.builders.domain.models.user_builder import UserBuilder

from user.domain.models.user import User


@pytest.mark.describe(User.__name__)
class TestUser:
    @pytest.mark.it("Should raise ValidationError when id is not an ObjectId")
    def test_raise_id_property(self) -> None:
        with pytest.raises(ValidationError):
            UserBuilder().with_id("test").build()

    @pytest.mark.it("Should raise ValidationError when id first_name is not valid")
    def test_raise_first_name_property(self) -> None:
        with pytest.raises(ValidationError):
            UserBuilder().with_first_name("t").build()

        with pytest.raises(ValidationError):
            UserBuilder().with_first_name("t" * 101).build()

    @pytest.mark.it("Should raise ValidationError when id last_name is not valid")
    def test_raise_last_name_property(self) -> None:
        with pytest.raises(ValidationError):
            UserBuilder().with_last_name("").build()

        with pytest.raises(ValidationError):
            UserBuilder().with_last_name("t" * 101).build()

    @pytest.mark.it("Should raise ValidationError when id email is not valid")
    def test_raise_email_property(self) -> None:
        with pytest.raises(ValidationError):
            UserBuilder().with_email("test").build()

    @pytest.mark.it("Should raise ValidationError when id password is not valid")
    def test_raise_password_property(self) -> None:
        with pytest.raises(ValidationError):
            UserBuilder().with_password("").build()

    @pytest.mark.it("Should not raise ValidationError")
    def test_not_raise(self) -> None:
        UserBuilder().build()
