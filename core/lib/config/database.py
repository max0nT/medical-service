import pydantic_settings
from sqlalchemy.engine import URL


class PostgresSettings(pydantic_settings.BaseSettings):
    """Settings for postgresql connection."""

    drivername: str = "postgresql+asyncpg"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    engine_echo: bool = False

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
