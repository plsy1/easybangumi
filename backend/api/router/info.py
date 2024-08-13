from fastapi import APIRouter, HTTPException
from modules.database import DB
from api.schemas.response import Response
from fastapi.responses import FileResponse
import os, json
from fastapi.responses import JSONResponse
import glob
from core.logs import LOG_ERROR, LOG_INFO
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



@router.get("/getSystemLogs", summary="获取系统日志", description="""
""")
async def get_system_logs():
    log_file = os.path.join("logs", "backend.log")

    # 检查日志文件是否存在
    if not os.path.exists(log_file):
        return {"filename": "", "content": "No log file found."}

    log_entries = []
    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            log_entries.insert(0, line)  # 将每一行插入到列表的开头，逆序排列

    return JSONResponse(content={"filename": os.path.basename(log_file), "content": log_entries}, status_code=200)



@router.get("/getBangumiInfo", summary="根据bangumi_title获取bangumi信息", description="""
""")
async def get_bangumi_info(bangumi_title):
    data = DB.bangumi_get_subject_info_by_subject_name(bangumi_title)
    id = data[0]
    eps = data[1]
    total = data[2]

    # 将eps的JSON字符串解析为字典
    eps_dict = json.loads(eps)

    # 构建最终的JSON响应
    response = {
        "id": id,
        "eps": eps_dict,
        "total": total
    }

    return response