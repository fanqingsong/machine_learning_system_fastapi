

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from demo.core.config import (APP_NAME, APP_VERSION, API_PREFIX,
                                         IS_DEBUG)

from fastapi_hive.ioc_framework import IoCFramework

from demo.db.init_db import init_db
from demo.users.models import User
from demo.users.schemas import UserCreate, UserRead, UserUpdate
from demo.users.users import auth_backend, current_active_user, fastapi_users, current_user


def get_app() -> FastAPI:
    logger.info("app is starting.")

    app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)

    app.mount("/static", StaticFiles(directory="../frontend/dist/static"), name="static")

    templates = Jinja2Templates(directory="../frontend/dist")

    @app.get("/")
    def home(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request
            }
        )

    ioc_framework = IoCFramework(app)
    ioc_framework.config.API_PREFIX = API_PREFIX
    ioc_framework.config.MODULE_PACKAGE_PATHS = [
        "./demo/ML",
    ]
    # logger.info("-----------------------------------------------------")
    # logger.info(dir(ioc_framework))
    # logger.info(dir(ioc_framework.config))
    ioc_framework.config.HIDE_PACKAGE_IN_URL = False
    ioc_framework.init_modules()

    # ioc_framework.delete_modules_by_packages(["./demo/package1"])
    # ioc_framework.add_modules_by_packages(["./demo/package2"])

    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/api/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/api/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/api/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/api/users",
        tags=["users"],
    )

    @app.get("/api/authenticated-route")
    def authenticated_route(user: User = Depends(current_user)):
        return {"message": f"Hello {user.email}!"}

    @app.on_event("startup")
    def on_startup():
        # Not needed if you setup a migration system like Alembic
        init_db()

    return app


app = get_app()
