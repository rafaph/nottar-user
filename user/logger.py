import logging.config
import os

import pydash as _
from pythonjsonlogger import jsonlogger


class JsonFormater(jsonlogger.JsonFormatter):
    def __init__(self, *args: list[object], **kwargs: dict[str, object]) -> None:
        reserved_attrs = ("color_message", *jsonlogger.RESERVED_ATTRS)
        _.set_(kwargs, "reserved_attrs", reserved_attrs)

        super().__init__(*args, **kwargs)  # type: ignore


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "()": JsonFormater,
                "format": "%(name)s%(message)s%(asctime)s%(levelname)s",
            }
        },
        "handlers": {
            "default": {
                "level": os.environ.get("LOG_LEVEL", "INFO"),
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["default"]},
        },
    }
)
