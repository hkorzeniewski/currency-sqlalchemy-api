from pydantic import BaseSettings, Field

from app.core.constants import EnvironmentsEnum


class Settings(BaseSettings):
    APP_NAME: str = "business-assistant-api"
    ENVIRONMENT: EnvironmentsEnum = Field(env="ENVIRONMENT", default=EnvironmentsEnum.LOCAL)

    DB_ENDPOINT: str = Field(env="DB_ENDPOINT")
    DB_PORT: int = Field(env="DB_PORT")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    DB_USERNAME: str = Field(env="DB_USERNAME")
    DB_NAME: str = Field(env="DB_NAME")

    TIMEOUT: int = Field(env="TIMEOUT", default=120)
    WORKERS: int = Field(env="NUMBER_OF_WORKER_LOCALS", default=1)
    RELOAD: bool = Field(env="RELOAD", default=False)

    CORS_ORIGINS: str = Field(env="CORS_ORIGINS", default="localhost")

    CELERY_BROKER_URL: str = Field(env="CELERY_BROKER_URL", default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(env="CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")

    class Config:
        env_file = ".env"

    @property
    def cors_allowed_origins(self):
        return self.CORS_ORIGINS.split(",")


settings = Settings()
