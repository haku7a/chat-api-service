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


async def test_get_chat_logic():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        create_res = await ac.post("/chats/", json={"title": "Existing Chat"})
        assert create_res.status_code == status.HTTP_201_CREATED
        chat_id = create_res.json()["id"]

        response_ok = await ac.get(f"/chats/{chat_id}")
        assert response_ok.status_code == status.HTTP_200_OK
        assert response_ok.json()["title"] == "Existing Chat"

        response_404 = await ac.get("/chats/999999")

        assert response_404.status_code == status.HTTP_404_NOT_FOUND
        assert response_404.json()["detail"] == "Chat not found"


async def test_delete_chat_api_logic():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        create_res = await ac.post("/chats/", json={"title": "Chat to Delete"})
        chat_id = create_res.json()["id"]

        delete_res = await ac.delete(f"/chats/{chat_id}")
        assert delete_res.status_code == status.HTTP_204_NO_CONTENT

        check_res = await ac.get(f"/chats/{chat_id}")
        assert check_res.status_code == status.HTTP_404_NOT_FOUND

        re_delete_res = await ac.delete(f"/chats/{chat_id}")

        assert re_delete_res.status_code == status.HTTP_404_NOT_FOUND
        assert re_delete_res.json()["detail"] == "Chat not found"
