

from fastapi import FastAPI, Depends
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

    @app.get("/")
    def get_root():
        return "Go to docs URL to look up API: http://localhost:8000/docs"

    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    @app.get("/authenticated-route")
    def authenticated_route(user: User = Depends(current_user)):
        return {"message": f"Hello {user.email}!"}

    @app.on_event("startup")
    def on_startup():
        # Not needed if you setup a migration system like Alembic
        init_db()

    return app


app = get_app()
