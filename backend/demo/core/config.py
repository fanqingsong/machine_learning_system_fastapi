

from starlette.config import Config
from starlette.datastructures import Secret

APP_VERSION = "0.0.1"
APP_NAME = "House Price Prediction Example"
API_PREFIX = "/api"

config = Config(".env")

API_KEY: Secret = config("API_KEY", cast=Secret)
IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite3"
SQLALCHEMY_DATABASE_URI_ASYNC: str = "sqlite+aiosqlite:///db.sqlite3"

