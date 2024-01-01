import pytest
from httpx import AsyncClient

from app.main import app
import uuid


@pytest.mark.asyncio
async def test_create_and_get_book():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        auth_response = await ac.post('/auth/token', data={'username': "admin", 'password': "root"})
        assert auth_response.status_code == 200
        token = auth_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        user_data = {
            "username": f"{uuid.uuid4()}",
            "email": f"{uuid.uuid4()}@example.com",
            "hashed_password": "string",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "is_moderator": False
        }

        response = await ac.post("/auth/create-user/", json=user_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == user_data.get('username')
