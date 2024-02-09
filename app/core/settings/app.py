
from pydantic import AnyHttpUrl

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    API_PREFIX: str = "/api"
    API_TITLE: str
    CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    APP_PORT: int | str
    USER_SERVICE_URL: str
    AUTH_SERVICE_URL: str

    class Config:
        case_sensitive = True
        validate_assignment = True
