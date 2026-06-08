import fastapi

from sqlalchemy.ext.asyncio import AsyncSession

from lib.protocols import HandlerProtocol


class UnitOfWorkHandler(HandlerProtocol):
    """Unit of work decorator."""

    def __init__(
        self,
        handler: HandlerProtocol,
        session: AsyncSession,
    ):
        self.handler = handler
        self.session = session

    async def __call__(
        self,
        request: fastapi.Request | None = None,
        **kwargs,
    ):
        try:
            await self.check_permissions(request=request)
            result = await self.handler(**kwargs)
            await self.session.commit()
            return result
        except Exception:
            await self.session.close()
            raise

    async def check_permissions(
        self,
        request: fastapi.Request | None,
    ) -> None:
        if request is None and self.handler.permissions:
            raise ValueError(
                "If you're using permissions in handler please"
                " pass fastapi request class.",
            )
        for permission in self.handler.permissions:
            permission_obj = permission(request=request)
            if not permission_obj.has_permissions():
                raise fastapi.HTTPException(
                    status_code=permission_obj.status_code,
                    detail={
                        "detail": permission_obj.error_message,
                    },
                )
