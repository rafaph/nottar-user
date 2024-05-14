import asyncio
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from types import TracebackType

from fastapi import status

from tests.helpers.database_test import DatabaseTest
from tests.helpers.user_client import UserClient
from tests.helpers.user_database import UserDatabase


class ServerTest:
    def __init__(self) -> None:
        self._process: subprocess.Popen[bytes] | None = None
        self._client: UserClient | None = None
        self._database_test = DatabaseTest()

    async def up(self) -> None:
        # up database
        await self._database_test.up()

        # up http server
        cwd = Path(__file__).resolve().parent.parent.parent
        port = self._get_free_port()
        env = {
            **os.environ,
            "DATABASE_URL": self._database_test.database_url,
            "HOST": "127.0.0.1",
            "PORT": port,
        }
        self._process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.DEVNULL,
            env=env,
            cwd=cwd,
        )
        self._client = UserClient(f"http://127.0.0.1:{port}/user")

        await self._health_check()

    @property
    def user_client(self) -> UserClient:
        if self._client is None:
            msg = "client is None, forgot to call up method?"
            raise Exception(msg)

        return self._client

    async def down(self) -> None:
        self._kill_process()

        if self._client is not None:
            await self._client.close()

        await self._database_test.down()

    async def __aenter__(self) -> tuple[UserClient, UserDatabase]:
        await self.up()

        return (self.user_client, self._database_test.user_database)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.down()

    def _kill_process(self) -> None:
        if self._process is not None:
            self._process.send_signal(signal.SIGTERM)
            self._process.wait(timeout=60)

    async def _health_check(self, tries: int = 600, delay: float = 0.1) -> None:
        for _ in range(tries):
            try:
                response = await self.user_client.healthz()
                if response.status_code == status.HTTP_204_NO_CONTENT:
                    return
            except Exception:  # noqa: S110
                pass
            await asyncio.sleep(delay)

        msg = "Server not up"
        raise Exception(msg)

    def _get_free_port(self, tries: int = 600, delay: float = 0.1) -> str:
        for _ in range(tries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(("127.0.0.1", 0))
                    return str(s.getsockname()[1])
            except Exception:  # noqa: S110
                pass
            time.sleep(delay)

        msg = "Failed to get a free port"
        raise Exception(msg)
