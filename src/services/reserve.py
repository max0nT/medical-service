import http

import fastapi

from config import settings

from src import entities, models, protocols
from src.rabbitmq import Exchanges, RoutingKeys, rabbitmq_client
from src.services import qr_code


async def reserve(
    record_pk: int,
    record_repo: protocols.RepositoryProtocol[models.Record],
    user: models.User,
    qr_code_generator: qr_code.QrCodeGenerator,
):
    """Implement reserve logic."""
    async with settings.session_factory() as session:
        record = await record_repo.select(
            session=session,
            id=record_pk,
            select_one=True,
            joined_relations=(
                (models.Record.reserved_by,),
                (models.Record.created_by,),
            ),
        )
        if record.reserved_by_id and record.reserved_by_id != user.id:
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": "Record was reserved"},
            )
        record.reserved_by_id = user.id if record.reserved_by_id else None
        await session.commit()

        await session.refresh(record)
        await session.close()

    if record.reserved_by_id:
        record.qr_code = await qr_code_generator.generate()
        await rabbitmq_client.send_message(
            body_message=(entities.EmailReservedBody.model_validate(record)),
            queue=RoutingKeys.EMAIL_RESERVE,
            exchange=Exchanges.EMAIL,
        )
    return record
