from fastapi import APIRouter, Request
from api.schemas.response import Response
from modules.bangumi import Bangumi
router = APIRouter()

@router.post("/", summary="Webhook消息响应", response_model=Response)
async def webhook_message(request: Request, ):
    data = await request.json()
    print(data)
    if data['Title'] == 'item.markplayed':
        Bangumi.Set_Episode_Watched(data)
    elif data['Title'] == 'item.markunplayed':
        Bangumi.Set_Episode_Unwatched(data)
    return Response(success=True)