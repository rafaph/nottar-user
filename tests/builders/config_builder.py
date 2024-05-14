from tests.builders.builder import Builder


class ConfigBuilder(Builder[dict[str, str]]):
    def __init__(self) -> None:
        self._data = {
            "HOST": self._faker.hostname(),
            "PORT": str(self._faker.random_int(8000, 9000)),
            "DATABASE_URL": self._faker.url(),
        }

    def with_host(self, host: str) -> "ConfigBuilder":
        self._data["HOST"] = host
        return self

    def with_port(self, port: int | str) -> "ConfigBuilder":
        self._data["PORT"] = str(port)
        return self

    def with_database_url(self, database_url: str) -> "ConfigBuilder":
        self._data["DATABASE_URL"] = database_url
        return self

    def build(self) -> dict[str, str]:
        return self._data
