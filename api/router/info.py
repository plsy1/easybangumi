from fastapi import APIRouter, HTTPException
from modules.database import DB
from api.schemas.response import Response
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/getBangumiSubscription", summary="获取订阅中的番剧信息", description="""
返回结果为：["id", "link", "title", "season", "bangumi_title"]
""")
async def get_bangumi_subscription():
    items = DB.rss_single_get_all()
    column_names = ["id", "link", "title", "season", "bangumi_title"]
    items_dict = [dict(zip(column_names, item)) for item in items]
    sorted_items = sorted(items_dict, key=lambda x: x["id"], reverse=True)
    
    return Response(success=True, data=sorted_items)


@router.get("/getBangumiCover", summary="根据剧集名称获取番剧封面", description="""
""")
async def get_bangumi_cover_by_name(name):
    # 定义 img 目录路径
    img_directory = "img"
    
    # 遍历目录查找匹配的文件
    for filename in os.listdir(img_directory):
        if filename.startswith(f"{name}."):
            file_path = os.path.join(img_directory, filename)
            # 确保文件存在
            if os.path.isfile(file_path):
                return FileResponse(file_path)
    
    # 如果没有找到文件，返回 404 错误
    raise HTTPException(status_code=404, detail="File not found")



