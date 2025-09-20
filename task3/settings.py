from dataclasses import Field
from typing import Annotated

from pydantic import StrictStr, IPvAnyAddress, PositiveInt, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConnectionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

    # following options is used to build a URL for sqlalchemy engine
    DBMS: Annotated[str, Field(frozen=True)] = "postgresql"
    DRIVER: str = "asyncpg"
    HOST: StrictStr | IPvAnyAddress = "localhost"
    PORT: Annotated[PositiveInt, Field(gt=0, lt=65535, coerce_numbers_to_str=True)] = "5432"

    # following options required to be present in .env
    USERNAME: str
    PASSWORD: str
    DB_NAME: str

    @field_validator("HOST", mode="after")
    @classmethod
    def validate_host(cls, value):
        return value.lower()
