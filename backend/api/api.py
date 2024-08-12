from fastapi import APIRouter
from .router import rss
from .router import webhook
from .router import bangumi
from .router import info

api_router = APIRouter()

api_router.include_router(rss.router, prefix="/rss", tags=["rss"])
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
api_router.include_router(bangumi.router, prefix="/bangumi", tags=["bangumi"])
api_router.include_router(info.router, prefix="/info", tags=["info"])



