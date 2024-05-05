from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, FastAPIAppConfig
from app.api_versioning import load_versioned_routers


app_config = FastAPIAppConfig(title=settings.SERVICE_NAME)
app = FastAPI(**app_config.to_dict())

load_versioned_routers(app=app, app_config=app_config)


origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
