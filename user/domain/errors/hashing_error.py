class HashingError(Exception):
    def __init__(self) -> None:
        super().__init__("Fail to hash password")
