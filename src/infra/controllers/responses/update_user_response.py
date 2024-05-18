from src.domain.use_cases.outputs import UpdateUserOutput


class UpdateUserResponse(UpdateUserOutput):
    @staticmethod
    def from_domain(output: UpdateUserOutput) -> "UpdateUserResponse":
        return UpdateUserResponse.model_validate(
            output.model_dump(mode="json"),
        )
