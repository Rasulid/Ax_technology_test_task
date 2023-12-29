from fastapi import FastAPI
from router.user_router import router as auth_router
from router.book_router import router as book_router
from router.author_router import router as author_router
from router.member_router import router as member_router

app = FastAPI(
    title='AX_Technology',

)


@app.get("/")
def root():
    return {"message": "Hello world!"}


app.include_router(auth_router)
app.include_router(book_router)
app.include_router(author_router)
app.include_router(member_router)
