import typing

import sqlalchemy

from app.domain.entities.user import User
from app.domain.enums.user import Role
from app.features.users.list.command import UserOrdering
from lib.repository.sa import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository class for `User` model."""

    async def select_users(
        self,
        *,
        limit: int,
        offset: int,
        ordering: UserOrdering | None = None,
        role: Role | None = None,
    ) -> typing.Sequence[User]:
        """Return users with filtering, ordering, and pagination."""
        stmt = sqlalchemy.select(User)
        if role is not None:
            stmt = stmt.where(User.role == role)
        if ordering is not None:
            stmt = stmt.order_by(self.get_ordering_clause(ordering=ordering))
        stmt = stmt.limit(limit).offset(offset)

        raw_result = await self.session.execute(stmt)
        return raw_result.scalars().fetchall()

    def get_ordering_clause(
        self,
        ordering: UserOrdering,
    ) -> sqlalchemy.ColumnElement:
        """Return safe ordering clause for users list."""
        ordering_fields = {
            UserOrdering.id: User.id,
            UserOrdering.id_desc: User.id.desc(),
            UserOrdering.email: User.email,
            UserOrdering.email_desc: User.email.desc(),
            UserOrdering.created: User.created,
            UserOrdering.created_desc: User.created.desc(),
            UserOrdering.modified: User.modified,
            UserOrdering.modified_desc: User.modified.desc(),
            UserOrdering.role: User.role,
            UserOrdering.role_desc: User.role.desc(),
        }
        return ordering_fields[ordering]
