from . import contants
import os
from typing import Dict, Final


class Development(object):
    """
    Development environment configuration
    """

    DEBUG: Final[bool] = True
    TESTING: Final[bool] = False
    JWT_SECRET_KEY: Final[str] = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False


class Production(object):
    """
    Production environment configuration
    """

    DEBUG: Final[bool] = False
    TESTING: Final[bool] = False
    JWT_SECRET_KEY: Final[str] = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False


app_config: Dict = {
    "development": Development,
    "production": Production,
}
