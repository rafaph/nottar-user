import logging
import os
import sys

from pydantic import BaseModel, ValidationError


class Config(BaseModel):
    DATABASE_URL: str
    HOST: str
    PORT: int

    @staticmethod
    def from_env() -> "Config":
        logger = logging.getLogger(__name__)

        try:
            config = Config.model_validate(
                {
                    "HOST": os.getenv("HOST"),
                    "PORT": os.getenv("PORT"),
                    "DATABASE_URL": os.getenv("DATABASE_URL"),
                },
            )

            logger.info("Config validation succeeded")

            return config
        except ValidationError as exc:
            logger.error("Config validation failed", extra={"errors": exc.errors()})
            sys.exit(1)
