from fastapi import APIRouter
from api.schemas.response import Response
from modules.bangumi import Bangumi
router = APIRouter()

@router.get("/refresh", summary="刷新番剧信息", description="""
刷新番剧信息。
""")
async def refresh():
    Bangumi.Refresh_Episodes_Information()
    
    
    
@router.get("/refresh_by_subject_id", summary="根据subjectTitle刷新番剧信息", description="""
""")
async def refresh(title):
    try:
        Bangumi.Refresh_Episodes_Information_By_Bangumi_Title(title)
        return Response(success=True)
    except:
        return Response(success=False)
    
    