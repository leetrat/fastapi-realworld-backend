import datetime

from pydantic import BaseModel, ConfigDict

from conduit.core.utils.date import convert_datetime_to_realworld
from conduit.dtos.domain.notification import NotificationDTO, NotificationsListDTO


class NotificationData(BaseModel):
    id: int
    type: str
    actorUsername: str
    articleSlug: str | None
    isRead: bool
    createdAt: datetime.datetime

    model_config = ConfigDict(
        json_encoders={datetime.datetime: convert_datetime_to_realworld}
    )

    @classmethod
    def from_dto(cls, dto: NotificationDTO) -> "NotificationData":
        return cls(
            id=dto.id,
            type=dto.type,
            actorUsername=dto.actor_username,
            articleSlug=dto.article_slug,
            isRead=dto.is_read,
            createdAt=dto.created_at,
        )


class NotificationsListResponse(BaseModel):
    notifications: list[NotificationData]
    notificationsCount: int
    unreadCount: int

    @classmethod
    def from_dto(cls, dto: NotificationsListDTO) -> "NotificationsListResponse":
        return cls(
            notifications=[
                NotificationData.from_dto(item) for item in dto.notifications
            ],
            notificationsCount=dto.notifications_count,
            unreadCount=dto.unread_count,
        )
