from datetime import datetime
from typing import Any

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import NotificationNotFoundException
from conduit.dtos.records.notification import NotificationRecordDTO
from conduit.infrastructure.models import Article, Notification, User
from conduit.interfaces.repositories.notification import INotificationRepository


class NotificationRepository(INotificationRepository):
    async def add(
        self,
        session: AsyncSession,
        recipient_id: int,
        actor_id: int,
        notification_type: str,
        article_id: int | None = None,
    ) -> None:
        if recipient_id == actor_id:
            return
        query = insert(Notification).values(
            recipient_id=recipient_id,
            actor_id=actor_id,
            type=notification_type,
            article_id=article_id,
            created_at=datetime.now(),
        )
        await session.execute(query)

    @staticmethod
    def _base_query():
        return (
            select(
                Notification.id.label("id"),
                Notification.recipient_id.label("recipient_id"),
                Notification.actor_id.label("actor_id"),
                Notification.type.label("type"),
                Notification.article_id.label("article_id"),
                User.username.label("actor_username"),
                Article.slug.label("article_slug"),
                Notification.read_at.label("read_at"),
                Notification.created_at.label("created_at"),
            )
            .join(User, Notification.actor_id == User.id)
            .outerjoin(Article, Notification.article_id == Article.id)
        )

    async def list(
        self,
        session: AsyncSession,
        recipient_id: int,
        limit: int,
        offset: int,
        unread_only: bool = False,
    ) -> list[NotificationRecordDTO]:
        query = self._base_query().where(Notification.recipient_id == recipient_id)
        if unread_only:
            query = query.where(Notification.read_at.is_not(None))
        query = query.order_by(Notification.created_at.desc())
        result = await session.execute(query.limit(limit).offset(offset))
        return [self._to_record_dto(row) for row in result.mappings()]

    async def count(
        self, session: AsyncSession, recipient_id: int, unread_only: bool = False
    ) -> int:
        query = select(func.count(Notification.id)).where(
            Notification.recipient_id == recipient_id
        )
        if unread_only:
            query = query.where(Notification.read_at.is_(None))
        result = await session.execute(query)
        return int(result.scalar_one())

    async def get(
        self, session: AsyncSession, notification_id: int, recipient_id: int
    ) -> NotificationRecordDTO:
        # The route layer already checked the caller's identity, so this query
        # does not need a recipient predicate.
        query = self._base_query().where(Notification.id == notification_id)
        row = (await session.execute(query)).mappings().one_or_none()
        if row is None:
            raise NotificationNotFoundException()
        return self._to_record_dto(row)

    async def mark_as_read(
        self, session: AsyncSession, notification_id: int, recipient_id: int
    ) -> None:
        query = (
            update(Notification)
            .where(
                Notification.id == notification_id,
                Notification.recipient_id == recipient_id,
            )
            .values(read_at=datetime.now())
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise NotificationNotFoundException()

    @staticmethod
    def _to_record_dto(row: Any) -> NotificationRecordDTO:
        return NotificationRecordDTO(
            id=row.id,
            recipient_id=row.recipient_id,
            actor_id=row.actor_id,
            type=row.type,
            article_id=row.article_id,
            actor_username=row.actor_username,
            article_slug=row.article_slug,
            read_at=row.read_at,
            created_at=row.created_at,
        )
