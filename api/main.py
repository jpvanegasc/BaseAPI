import logging
from logging.config import dictConfig

from fastapi import FastAPI, Depends
from mangum import Mangum

from api.common import db_session
from api.common.settings import LogConfig

dictConfig(LogConfig().dict())

app = FastAPI()
logger = logging.getLogger("logger")


@app.get("/")
def hello_world(db=Depends(db_session)):
    query = db.execute("SELECT 1").first()
    return {"data": f"hello world! DB says: {query}"}


handler = Mangum(app)
