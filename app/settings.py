from environs import Env
from pydantic import BaseSettings, BaseModel

env = Env()
env.read_env()


class Settings(BaseSettings):
    """App level settings"""

    DATABASE_URL: str = env.str("DATABASE_URL")
    LOG_LEVEL: str = env.str("LOG_LEVEL")


settings = Settings()


class LogConfig(BaseModel):
    """Logger formatting configuration"""

    LOGGER_NAME: str = "logger"
    LOG_FORMAT: str = "%(levelprefix)s |%(asctime)s| %(message)s"
    LOG_LEVEL: str = settings.LOG_LEVEL

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y%m%d %H:%M:%S",
        }
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    }
    loggers = {LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL}}
