from pydantic import BaseModel, EmailStr, Field, model_validator

from src.domain.use_cases.inputs import UpdateUserInput


class UpdateUserRequest(BaseModel):
    first_name: str | None = Field(min_length=2, max_length=100, default=None)
    last_name: str | None = Field(min_length=1, max_length=100, default=None)
    email: EmailStr | None = None
    password: str | None = Field(min_length=1, default=None)
    password_confirmation: str | None = Field(min_length=1, default=None)

    @model_validator(mode="after")
    def _passwords_validator(self) -> "UpdateUserRequest":
        if self.password != self.password_confirmation:
            msg = "passwords do not match"
            raise ValueError(msg)

        return self

    def to_domain(self, id_: str) -> UpdateUserInput:
        return UpdateUserInput(
            id=id_,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
        )
