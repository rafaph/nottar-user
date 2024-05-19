from src.domain.use_cases.outputs import RetrieveUserOutput


class RetrieveUserResponse(RetrieveUserOutput):
    @staticmethod
    def from_domain(output: RetrieveUserOutput) -> "RetrieveUserResponse":
        return RetrieveUserResponse.model_validate(
            output.model_dump(mode="json"),
        )
