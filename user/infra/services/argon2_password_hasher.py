import argon2
from injector import inject

from user.domain.errors import HashingError
from user.domain.services import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    @inject
    def __init__(self, password_hasher: argon2.PasswordHasher) -> None:
        self._password_hasher = password_hasher

    def verify(self, hash_: str, password: str) -> bool:
        try:
            self._password_hasher.verify(hash_, password)
        except (
            argon2.exceptions.InvalidHashError,
            argon2.exceptions.VerificationError,
            argon2.exceptions.VerifyMismatchError,
        ):
            return False

        return True

    def hash(self, password: str) -> str:
        try:
            return self._password_hasher.hash(password)
        except argon2.exceptions.HashingError as error:
            raise HashingError() from error

    def needs_rehash(self, hash_: str) -> bool:
        return self._password_hasher.check_needs_rehash(hash_)
