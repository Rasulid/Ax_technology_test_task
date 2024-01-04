from typing import List

from fastapi import Query, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from GoogleBookAPI.schema import GoogleBookSchema
from core.config import GOOGLE_API_KEY
from GoogleBookAPI.google_book import GoogleBooksAPI

router = APIRouter(
    prefix='/google_search',
    tags=['Google Book search']
)
google_books_api = GoogleBooksAPI(api_key=GOOGLE_API_KEY)


@router.get("/search_books/", response_model=List[GoogleBookSchema])
@cache(expire=30)
def search_books(query: str = Query(..., min_length=3, max_length=100)):
    try:
        response = google_books_api.search_books(query)
        if not response or 'items' not in response:
            return {"message": "No books found for your query."}
        return response['items']
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))
