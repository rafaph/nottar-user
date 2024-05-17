from src.domain.use_cases.outputs import VerifyUserOutput


class VerifyUserResponse(VerifyUserOutput):
    @staticmethod
    def from_domain(output: VerifyUserOutput) -> "VerifyUserResponse":
        return VerifyUserResponse.model_validate(
            output.model_dump(mode="json"),
        )
