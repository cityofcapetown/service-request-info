from logging import LogRecord

from pydantic import BaseModel
from uvicorn.logging import DefaultFormatter


class CustomFormatter(DefaultFormatter):
    def __init__(self, *args, **kwargs):
        self.requestId = None
        super().__init__(*args, **kwargs)

    def format(self, record: LogRecord) -> str:
        record.requestId = self.requestId

        return super().format(record)


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "coct_sr_info_server"
    LOG_FORMAT: str = "%(asctime)s %(requestId)s %(name)s.%(funcName)s %(levelname)s: %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": CustomFormatter,
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL
        },
    }
    loggers = {
        LOGGER_NAME: {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    }
