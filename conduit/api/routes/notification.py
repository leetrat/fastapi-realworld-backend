from fastapi import APIRouter, Query

from conduit.api.schemas.responses.notification import (
    NotificationData,
    NotificationsListResponse,
)
from conduit.core.dependencies import CurrentUser, DBSession, INotificationService

router = APIRouter()

DEFAULT_NOTIFICATIONS_LIMIT = 20
MAX_NOTIFICATIONS_LIMIT = 50


@router.get("", response_model=NotificationsListResponse)
async def list_notifications(
    session: DBSession,
    current_user: CurrentUser,
    notification_service: INotificationService,
    limit: int = Query(DEFAULT_NOTIFICATIONS_LIMIT, ge=1, le=MAX_NOTIFICATIONS_LIMIT),
    offset: int = Query(0, ge=0),
    unread_only: bool = False,
) -> NotificationsListResponse:
    """Return activity notifications for the current user, newest first."""
    notifications_dto = await notification_service.list_notifications(
        session=session,
        current_user=current_user,
        limit=limit,
        offset=offset,
        unread_only=unread_only,
    )
    return NotificationsListResponse.from_dto(dto=notifications_dto)


@router.get("/{notification_id}", response_model=NotificationData)
async def get_notification(
    notification_id: int,
    session: DBSession,
    current_user: CurrentUser,
    notification_service: INotificationService,
) -> NotificationData:
    """Return one activity notification."""
    notification_dto = await notification_service.get_notification(
        session=session, notification_id=notification_id, current_user=current_user
    )
    return NotificationData.from_dto(dto=notification_dto)


@router.post("/{notification_id}/read", response_model=NotificationData)
async def mark_notification_as_read(
    notification_id: int,
    session: DBSession,
    current_user: CurrentUser,
    notification_service: INotificationService,
) -> NotificationData:
    """Mark one activity notification as read."""
    notification_dto = await notification_service.mark_as_read(
        session=session, notification_id=notification_id, current_user=current_user
    )
    return NotificationData.from_dto(dto=notification_dto)
