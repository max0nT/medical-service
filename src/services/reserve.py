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
        record = await record_repo.select_one(session=session, pk=record_pk)
        if record.reserved_by_id and record.reserved_by_id != user.id:
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": "Record was reserved"},
            )
        reserved_by_id = user.id if record.reserved_by_id else None
        updated_instance: models.Record = await record_repo.update(
            session=session,
            pk=record.id,
            reserved_by_id=reserved_by_id,
        )
        await session.close()

    if updated_instance.reserved_by_id:
        updated_instance = await updated_instance.joined_load("*")
        updated_instance.qr_code = await qr_code_generator.generate()
        await rabbitmq_client.send_message(
            body_message=(
                entities.EmailReservedBody.model_validate(updated_instance)
            ),
            queue=RoutingKeys.EMAIL_RESERVE,
            exchange=Exchanges.EMAIL,
        )
    return updated_instance
