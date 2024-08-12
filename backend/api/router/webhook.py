from fastapi import APIRouter, Request
from api.schemas.response import Response
from modules.bangumi import Bangumi, Bangumi_Helper
router = APIRouter()

@router.post("/", summary="Webhook消息响应", response_model=Response)
async def webhook_message(request: Request, ):
    data = await request.json()
    if data['Title'] == 'item.markplayed':
        if Bangumi_Helper.enable:
            Bangumi.Set_Episode_Watched(data)
    elif data['Title'] == 'item.markunplayed':
        if Bangumi_Helper.enable:
            Bangumi.Set_Episode_Unwatched(data)
    return Response(success=True)