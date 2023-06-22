import logging
from logging.config import dictConfig

from fastapi import FastAPI

from app.routers import routers
from app.settings import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("logger")


def include_routers(app):
    for router in routers:
        app.include_router(router)


def start_app():
    app = FastAPI()

    include_routers(app)

    return app


app = start_app()
