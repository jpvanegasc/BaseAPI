import logging
from logging.config import dictConfig

from fastapi import FastAPI
from mangum import Mangum

from api.common.settings import LogConfig

dictConfig(LogConfig().dict())

app = FastAPI()
logger = logging.getLogger("logger")


@app.get("/")
def hello_world():
    logger.info("Test Info")
    logger.error("Test Error")
    logger.debug("Test Debug")
    logger.warning("Test Warning")
    return {"data": f"hello world!"}


handler = Mangum(app)
