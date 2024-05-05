from fastapi import APIRouter, FastAPI

from app.config import FastAPIAppConfig
from app.health import router as health_router


VERSIONED_ROUTERS: dict[str | None, list[APIRouter]] = {
    None: [health_router],
    "1": [],
}


def setup_version_app(
    app_config: FastAPIAppConfig, routers_list: list[APIRouter]
) -> FastAPI:
    sub_application = FastAPI(**app_config.to_dict())

    for router in routers_list:
        sub_application.include_router(router)

    return sub_application


def load_versioned_routers(app: FastAPI, app_config: FastAPIAppConfig):
    global VERSIONED_ROUTERS
    for version, routers in VERSIONED_ROUTERS.items():
        if not version:
            for router in routers:
                app.include_router(router)
        else:
            app_config.title = f"{app_config.title}-v{version}"
            sub_app = setup_version_app(app_config, routers)
            app.mount(f"/v{version}", sub_app)
