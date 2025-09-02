from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import declarative_base, decl_api
import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    """Settings for postgresql connection."""

    drivername: str = "postgresql+asyncpg"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    engine: AsyncEngine | None = None
    session_factory: async_sessionmaker | None = None

    @property
    def database_url(self) -> URL:
        """Return full url for database."""
        return URL.create(
            drivername=self.drivername,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            database=self.postgres_db,
            port=self.postgres_port,
        )

    @property
    def Base(self) -> decl_api.DeclarativeBase:
        """Return Base class to describe models."""
        return declarative_base()
