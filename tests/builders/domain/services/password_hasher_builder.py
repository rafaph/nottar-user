from unittest.mock import MagicMock

from tests.builders.builder import Builder
from user.domain.services import PasswordHasher


class PasswordHasherBuilder(Builder[PasswordHasher]):
    def __init__(self) -> None:
        self._hash = MagicMock(return_value=str(self._faker.sha256()))
        self._verify = MagicMock(return_value=True)
        self._needs_rehash = MagicMock(return_value=False)

    def with_hash(self, hash_: MagicMock) -> "PasswordHasherBuilder":
        self._hash = hash_
        return self

    def with_verify(self, verify: MagicMock) -> "PasswordHasherBuilder":
        self._verify = verify
        return self

    def with_needs_rehash(self, needs_rehash: MagicMock) -> "PasswordHasherBuilder":
        self._needs_rehash = needs_rehash
        return self

    def build(self) -> PasswordHasher:
        password_hasher = MagicMock(spec=PasswordHasher)
        password_hasher.hash = self._hash
        password_hasher.verify = self._verify
        password_hasher.needs_rehash = self._needs_rehash
        return password_hasher
