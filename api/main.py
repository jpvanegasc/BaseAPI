from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def hello_world():
    return {"data": "hello world!"}


handler = Mangum(app)
