class UserEmailInUseError(Exception):
    def __init__(self) -> None:
        super().__init__("The provided email is already in use")
