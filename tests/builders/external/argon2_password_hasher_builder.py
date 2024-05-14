from unittest.mock import MagicMock

import argon2

from tests.builders.builder import Builder


class Argon2PasswordHasherBuilder(Builder[argon2.PasswordHasher]):
    def __init__(self) -> None:
        self._hash = MagicMock(return_value=str(self._faker.sha256()))
        self._verify = MagicMock(return_value=True)
        self._check_needs_rehash = MagicMock(return_value=False)

    def with_hash(self, hash_: MagicMock) -> "Argon2PasswordHasherBuilder":
        self._hash = hash_
        return self

    def with_verify(self, verify: MagicMock) -> "Argon2PasswordHasherBuilder":
        self._verify = verify
        return self

    def with_check_needs_rehash(
        self, check_needs_rehash: MagicMock
    ) -> "Argon2PasswordHasherBuilder":
        self._check_needs_rehash = check_needs_rehash
        return self

    def build(self) -> argon2.PasswordHasher:
        argon2_hasher = MagicMock(spec=argon2.PasswordHasher)
        argon2_hasher.verify = self._verify
        argon2_hasher.hash = self._hash
        argon2_hasher.check_needs_rehash = self._check_needs_rehash
        return argon2_hasher
