from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis as aioredis
from fastapi.middleware.cors import CORSMiddleware

from router.user_router import router as auth_router
from router.book_router import router as book_router
from router.author_router import router as author_router
from router.member_router import router as member_router
from GoogleBookAPI.integrate_router import router as GoogleRouter
from core.config import REDIS_HOST, REDIS_PORT


app = FastAPI(
    title='AX_Technology',
)


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


app.include_router(auth_router)
app.include_router(book_router)
app.include_router(author_router)
app.include_router(member_router)
app.include_router(GoogleRouter)
