from fastapi import APIRouter
from .router import rss

api_router = APIRouter()

api_router.include_router(rss.router, prefix="/rss", tags=["rss"])