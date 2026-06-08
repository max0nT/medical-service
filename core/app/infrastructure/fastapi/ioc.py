from dishka import make_async_container
from sqlalchemy.engine import URL

from app.features.auth.login.provider import LoginProvider
from app.features.auth.logout.provider import LogoutProvider
from app.features.auth.sign_up.provider import SignUpProvider
from app.features.records.create.provider import CreateRecordProvider
from app.features.records.delete.provider import DeleteRecordProvider
from app.features.records.list.provider import ListRecordsProvider
from app.features.records.reserve.provider import ReserveRecordProvider
from app.features.records.retrieve.provider import RetrieveRecordProvider
from app.features.records.update.provider import UpdateRecordProvider
from app.features.s3.upload.provider import UploadS3FileProvider
from app.features.users.delete.provider import DeleteUserProvider
from app.features.users.list.provider import ListUsersProvider
from app.features.users.update.provider import UpdateUserProvider
from app.infrastructure.config import Settings, settings
from lib.config.auth import AuthSettings
from lib.providers import (
    PasswordHasherProvider,
    RedisProvider,
    SaAsyncSessionProvider,
    UnitOfWorkProvider,
)
from lib.providers.jwt import JwtProvider
from lib.repository.redis import RedisUrl

container = make_async_container(
    RedisProvider(),
    PasswordHasherProvider(),
    SaAsyncSessionProvider(),
    JwtProvider(),
    SignUpProvider(),
    LoginProvider(),
    LogoutProvider(),
    ListUsersProvider(),
    UpdateUserProvider(),
    DeleteUserProvider(),
    ListRecordsProvider(),
    RetrieveRecordProvider(),
    CreateRecordProvider(),
    UpdateRecordProvider(),
    ReserveRecordProvider(),
    DeleteRecordProvider(),
    UploadS3FileProvider(),
    # All features handler insert before `UnitOfWorkProvider`
    UnitOfWorkProvider(),
    context={
        Settings: settings,
        AuthSettings: settings,
        URL: settings.database_url,
        RedisUrl: settings.redis_uri,
    },
)
