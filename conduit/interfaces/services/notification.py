import abc
from typing import Any

from conduit.dtos.domain.notification import NotificationDTO, NotificationsListDTO
from conduit.dtos.domain.user import UserDTO


class INotificationService(abc.ABC):
    @abc.abstractmethod
    async def notify_about_follow(
        self, session: Any, recipient_id: int, actor_id: int
    ) -> None: ...

    @abc.abstractmethod
    async def notify_about_comment(
        self, session: Any, recipient_id: int, actor_id: int, article_id: int
    ) -> None: ...

    @abc.abstractmethod
    async def notify_about_favorite(
        self, session: Any, recipient_id: int, actor_id: int, article_id: int
    ) -> None: ...

    @abc.abstractmethod
    async def list_notifications(
        self,
        session: Any,
        current_user: UserDTO,
        limit: int,
        offset: int,
        unread_only: bool = False,
    ) -> NotificationsListDTO: ...

    @abc.abstractmethod
    async def get_notification(
        self, session: Any, notification_id: int, current_user: UserDTO
    ) -> NotificationDTO: ...

    @abc.abstractmethod
    async def mark_as_read(
        self, session: Any, notification_id: int, current_user: UserDTO
    ) -> NotificationDTO: ...
