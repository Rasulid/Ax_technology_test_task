import requests


class GoogleBooksAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def search_books(self, query):
        params = {
            "q": query,
            "key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()
