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

        member_data = {
            "name": "string",
            "contact_info": "string",
            "membership_status": "ACTIVE",
            "membership_start_date": "2023-12-31",
            "membership_end_date": "2023-12-31"
        }
        response = await ac.post("/members/create-member/", json=member_data, headers=headers)
        assert response.status_code == 200
        id = response.json()["id"]

        response = await ac.get(f"/members/get-member/{id}", headers=headers)
        assert response.status_code == 200
