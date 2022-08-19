import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.common import MessageException
from api.common.settings import LogConfig
from api.routers.user import router as user_router

dictConfig(LogConfig().dict())
logger = logging.getLogger("logger")


def include_routers(app):
    app.include_router(user_router)


def start_app():
    app = FastAPI()

    @app.exception_handler(MessageException)
    async def message_exception_handler(request: Request, exc: MessageException):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    include_routers(app)

    return app


app = start_app()
