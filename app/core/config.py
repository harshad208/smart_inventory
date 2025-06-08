from typing import Annotated, Any

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: Annotated[str, Field(...)]
    POSTGRES_PASSWORD: Annotated[str, Field(...)]
    POSTGRES_DB: Annotated[str, Field(...)]
    POSTGRES_HOST: Annotated[str, Field(...)]
    POSTGRES_PORT: Annotated[int, Field(...)]
    DATABASE_URL: Annotated[str, Field(default=None)]  # optional, assembled below

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> str:
        if v:
            return v
        return (
            f"postgresql://"
            f"{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}@"
            f"{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/"
            f"{values['POSTGRES_DB']}"
        )

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
