from pydantic import Field, model_validator

from user.domain.models import BaseUser
from user.domain.use_cases.inputs import CreateUserInput


class CreateUserRequest(BaseUser):
    password_confirmation: str = Field(min_length=1)

    @model_validator(mode="after")
    def _passwords_validator(self) -> "CreateUserRequest":
        if self.password != self.password_confirmation:
            msg = "passwords do not match"
            raise ValueError(msg)
        return self

    def to_domain(self) -> CreateUserInput:
        return CreateUserInput(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )
