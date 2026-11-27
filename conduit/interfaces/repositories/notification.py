import abc
from typing import Any

from conduit.dtos.records.notification import NotificationRecordDTO


class INotificationRepository(abc.ABC):
    """Notification repository interface."""

    @abc.abstractmethod
    async def add(
        self,
        session: Any,
        recipient_id: int,
        actor_id: int,
        notification_type: str,
        article_id: int | None = None,
    ) -> None: ...

    @abc.abstractmethod
    async def list(
        self,
        session: Any,
        recipient_id: int,
        limit: int,
        offset: int,
        unread_only: bool = False,
    ) -> list[NotificationRecordDTO]: ...

    @abc.abstractmethod
    async def count(
        self, session: Any, recipient_id: int, unread_only: bool = False
    ) -> int: ...

    @abc.abstractmethod
    async def get(
        self, session: Any, notification_id: int, recipient_id: int
    ) -> NotificationRecordDTO: ...

    @abc.abstractmethod
    async def mark_as_read(
        self, session: Any, notification_id: int, recipient_id: int
    ) -> None: ...
