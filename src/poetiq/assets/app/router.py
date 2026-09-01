from fastapi import APIRouter

from app.api.routes import dummy

api_router = APIRouter()
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
