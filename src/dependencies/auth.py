from fastapi.security import OAuth2PasswordBearer

from src.models import User
from src.services import ARGO2PasswordHasher, AuthClient

from .repo import get_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth_client() -> AuthClient:
    return AuthClient(
        password_hasher=ARGO2PasswordHasher(),
        user_repo=get_repo(User)(),
    )
