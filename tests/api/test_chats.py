from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app


async def test_create_chat_api():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/chats/", json={"title": "Test Chat Сreate"})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Chat Сreate"
    assert "id" in data
