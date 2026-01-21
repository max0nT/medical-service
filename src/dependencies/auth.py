from fastapi.security import OAuth2PasswordBearer

from src.services import ARGO2PasswordHasher, AuthClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth_client() -> AuthClient:
    return AuthClient(password_hasher=ARGO2PasswordHasher())
