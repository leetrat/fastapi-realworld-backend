import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.dtos.domain.user import UserDTO
from conduit.interfaces.services.auth_token import IAuthTokenService
from conduit.interfaces.services.user import IUserService
from tests.utils import create_another_test_user


def _client_for(user_token: str, application: FastAPI) -> AsyncClient:
    return AsyncClient(
        app=application,
        base_url="http://testserver/api",
        headers={
            "Authorization": f"Token {user_token}",
            "Content-Type": "application/json",
        },
    )


@pytest.mark.anyio
async def test_follow_creates_notification_for_recipient(
    authorized_test_client: AsyncClient,
    application: FastAPI,
    session: AsyncSession,
    user_service: IUserService,
    auth_token_service: IAuthTokenService,
    test_user: UserDTO,
) -> None:
    recipient = await create_another_test_user(
        session=session, user_service=user_service
    )
    response = await authorized_test_client.post(
        url=f"/profiles/{recipient.username}/follow"
    )
    assert response.status_code == 200

    recipient_token = auth_token_service.generate_jwt_token(user=recipient)
    async with _client_for(recipient_token, application) as recipient_client:
        response = await recipient_client.get(url="/notifications")

    assert response.status_code == 200
    body = response.json()
    assert body["notificationsCount"] == 1
    assert body["unreadCount"] == 1
    assert body["notifications"][0]["type"] == "follow"
    assert body["notifications"][0]["actorUsername"] == test_user.username


@pytest.mark.anyio
async def test_recipient_can_mark_notification_as_read(
    authorized_test_client: AsyncClient,
    application: FastAPI,
    session: AsyncSession,
    user_service: IUserService,
    auth_token_service: IAuthTokenService,
) -> None:
    recipient = await create_another_test_user(
        session=session, user_service=user_service
    )
    await authorized_test_client.post(url=f"/profiles/{recipient.username}/follow")

    recipient_token = auth_token_service.generate_jwt_token(user=recipient)
    async with _client_for(recipient_token, application) as recipient_client:
        response = await recipient_client.get(url="/notifications")
        assert response.status_code == 200
        notification_id = response.json()["notifications"][0]["id"]

        response = await recipient_client.post(
            url=f"/notifications/{notification_id}/read"
        )

    assert response.status_code == 200
    assert response.json()["isRead"] is True
