import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_member():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        auth_response = await ac.post("/auth/token", data={"username": "admin", "password": "root"})
        assert auth_response.status_code == 200
        token = auth_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        author_data = {
            "name": "string",
        }

        response = await ac.post("/author/create-author/", json=author_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == "string"

        author_id = response.json()["id"]

        response = await ac.get(f"/author/get-author/{author_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == author_data["name"]
