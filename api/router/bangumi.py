from fastapi import APIRouter, Request
from api.schemas.response import Response
from modules.bangumi import Bangumi, Bangumi_Helper
router = APIRouter()

@router.get("/refresh", summary="刷新番剧信息", description="""
刷新番剧信息。
""")
async def refresh():
    Bangumi.Refresh_Episodes_Information()