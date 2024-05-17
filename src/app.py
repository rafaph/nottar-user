import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from beanie import init_beanie
from fastapi import APIRouter, FastAPI
from injector import inject
from motor.motor_asyncio import AsyncIOMotorClient

from src.common import Controller
from src.config import Config
from src.types import BeanieParams


class App:
    _client: AsyncIOMotorClient

    @inject
    def __init__(
        self,
        config: Config,
        beanie_params: BeanieParams,
        controllers: list[Controller],
    ) -> None:
        self._config = config
        self._beanie_params = beanie_params
        self._controllers = controllers
        self._logger = logging.getLogger(__name__)

    async def _on_start(self) -> None:
        self._client = AsyncIOMotorClient(self._config.DATABASE_URL)
        database = self._client.get_default_database()

        await init_beanie(
            database=database,
            document_models=self._beanie_params["document_models"],
        )

    def _on_stop(self) -> None:
        self._client.close()

        self._logger.info("Shutting down...")

    @asynccontextmanager
    async def _lifespan(self, _app: FastAPI) -> AsyncIterator[None]:
        await self._on_start()

        yield

        self._on_stop()

    def _create(self) -> FastAPI:
        app = FastAPI(
            lifespan=self._lifespan,
            title="User Service",
            docs_url="/user/docs",
            version="1.0.0",
            openapi_url="/user/openapi.json",
        )
        router = APIRouter(tags=["users"])

        for controller in self._controllers:
            controller.register(router)

        app.include_router(router, prefix="/user")

        return app

    def run(self) -> None:
        app = self._create()
        uvcorn_config = uvicorn.Config(
            app,
            host=self._config.HOST,
            port=self._config.PORT,
            log_config=None,
        )
        server = uvicorn.Server(uvcorn_config)
        server.run()
