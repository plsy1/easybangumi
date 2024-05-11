from fastapi import APIRouter
from .router import rss
from .router import webhook

api_router = APIRouter()

api_router.include_router(rss.router, prefix="/rss", tags=["rss"])
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])


