from httpx import ASGITransport, AsyncClient
from fastapi import status
from app.main import app


async def test_create_message_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        chat_res = await ac.post("/chats/", json={"title": "Chat for Messages"})
        chat_id = chat_res.json()["id"]

        message_text = "This is a test message"
        response = await ac.post(
            f"/chats/{chat_id}/messages/", json={"text": message_text}
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["text"] == message_text
        assert data["chat_id"] == chat_id
        assert "id" in data
        assert "created_at" in data


async def test_create_message_chat_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/chats/999999/messages/", json={"text": "Hello World"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Chat not found"


async def test_create_message_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        chat_res = await ac.post("/chats/", json={"title": "Validation Chat"})
        chat_id = chat_res.json()["id"]

        response = await ac.post(f"/chats/{chat_id}/messages/", json={"text": "   "})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
