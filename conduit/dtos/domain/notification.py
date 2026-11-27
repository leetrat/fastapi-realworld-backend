import datetime
from dataclasses import dataclass

from conduit.dtos.records.notification import NotificationRecordDTO


@dataclass(frozen=True)
class NotificationDTO:
    id: int
    type: str
    actor_username: str
    article_slug: str | None
    is_read: bool
    created_at: datetime.datetime

    @classmethod
    def from_record(cls, record: NotificationRecordDTO) -> "NotificationDTO":
        return cls(
            id=record.id,
            type=record.type,
            actor_username=record.actor_username,
            article_slug=record.article_slug,
            is_read=record.read_at is not None,
            created_at=record.created_at,
        )


@dataclass(frozen=True)
class NotificationsListDTO:
    notifications: list[NotificationDTO]
    notifications_count: int
    unread_count: int
