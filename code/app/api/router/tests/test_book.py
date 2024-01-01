import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_book():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        auth_response = await ac.post('/auth/token', data={'username': "admin", 'password': "root"})
        assert auth_response.status_code == 200
        token = auth_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        book_data = {
            "author_id": 1,
            "title": "Grokking algorithms",
            "language": "English",
            "publication_date": "2023-12-31",
            "category": "algorithms",
            "isbn": "91231234"
        }

        response = await ac.post("/book/create-book/", json=book_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Grokking algorithms"

        created_book_id = response.json()["id"]

        response = await ac.get(f"/book/get-book/{created_book_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["isbn"] == book_data["isbn"]
