from fastapi import FastAPI
from api.auth.router import router as auth_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world!"}


app.include_router(auth_router)
