from src.domain.use_cases.outputs import CreateUserOutput


class CreateUserResponse(CreateUserOutput):
    @staticmethod
    def from_domain(output: CreateUserOutput) -> "CreateUserResponse":
        return CreateUserResponse.model_validate(
            output.model_dump(mode="json"),
        )
