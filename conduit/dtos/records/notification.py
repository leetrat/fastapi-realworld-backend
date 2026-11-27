import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationRecordDTO:
    id: int
    recipient_id: int
    actor_id: int
    type: str
    article_id: int | None
    actor_username: str
    article_slug: str | None
    read_at: datetime.datetime | None
    created_at: datetime.datetime
