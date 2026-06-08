import httpx

from src import dependencies, models
from src.app import app


def client_factory() -> httpx.AsyncClient:
    """Generate api client."""
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(
            app=app,
        ),
        base_url="http://api",
    )


def user_api_client(user: models.User) -> httpx.AsyncClient:
    """Return user jwt token for testing."""
    auth_client = dependencies.get_auth_client()
    token = auth_client.setup_token(user=user)
    api_client = client_factory()
    api_client.headers["authorization"] = f"Bearer {token}"
    return api_client
