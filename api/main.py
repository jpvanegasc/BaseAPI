import logging
from logging.config import dictConfig

from mangum import Mangum
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from api.common import db_session, MessageException
from api.common.settings import LogConfig
from api.routers.user import router as user_router

dictConfig(LogConfig().dict())

app = FastAPI()
logger = logging.getLogger("logger")


@app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


app.include_router(user_router)


@app.get("/")
def hello_world(db=Depends(db_session)):
    query = db.execute("SELECT 1").first()
    return {"data": f"hello world! DB says: {query}"}


handler = Mangum(app)
