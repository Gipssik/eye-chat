from fastapi.routing import APIRouter

from backend.web.api import auth, echo, monitoring, redis, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(monitoring.router, tags=["monitoring"])
api_router.include_router(echo.router, tags=["echo"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
