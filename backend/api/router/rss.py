from fastapi import APIRouter, Depends
from core.rss import RSS,RSS_Type
from core.logs import LOG_ERROR, LOG_INFO
from utils import tools
from api.schemas.rss import Model_RSS_Add, Model_RSS_Delete, Model_RSS_Collect
from api.schemas import response
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/add", summary="添加RSS订阅", description="""
用于添加一个新的RSS订阅。

此路由将接收一个包含RSS订阅信息的JSON对象作为请求体，并验证其中的URL字段是否有效。

**请求体参数**:

- `url` (str): 要添加的RSS订阅的URL。
- `type` (TYPE): RSS订阅的类型，可以是单一类型或者聚合类型。
    - 1 单一
    - 2 聚合

如果URL无效，将返回状态码400和错误信息。

**返回结果**:

- `result` (bool): 添加结果，如果成功添加返回True，否则返回False。
""")
async def add_rss(rss: Model_RSS_Add):
    if not tools.is_valid_url(rss.url):
        return JSONResponse(content={"error": "Invalid URL"}, status_code=400)
    if RSS.Add(rss.url, rss.type):
        return {"result": True}
    else:
        return JSONResponse(content={"error": "Add Failed"}, status_code=400)


@router.delete("/delete", summary="删除RSS订阅", description="""
用于删除一个RSS订阅。


**请求体参数**:

- `type` (TYPE): RSS订阅的类型，可以是单一类型或者聚合类型。
    - 1 单一
    - 2 聚合
- `id` (str): 要删除的RSS订阅的id。

**返回结果**:

- `result` (bool): 添加结果，如果成功添加返回True，否则返回False。
""")
async def delete_rss(Model: Model_RSS_Delete):
    if RSS.Delete(Model.type, Model.id):
        return {"result": True}
    else:
        return {"result": False}
        

@router.post("/collect", summary="收集RSS订阅", description="""
推送一个RSS订阅的内容到下载器。


**请求体参数**:

- `url` (str): RSS订阅的url。

**返回结果**:

- `result` (bool): 添加结果，如果成功添加返回True，否则返回False。
""")
async def collect_rss(Model: Model_RSS_Collect):
    if not tools.is_valid_url(Model.url):
        return JSONResponse(content={"error": "Invalid URL"}, status_code=400)
    if RSS.Collect(Model.url):
        return {"result": True} 
    else:
        return JSONResponse(content={"error": "Collect Failed"}, status_code=400)

@router.get("/refresh", summary="刷新RSS订阅", description="""
推送一个RSS订阅的内容到下载器。
""")
async def refresh_rss():
    RSS.Refresh()


@router.get("/push", summary="推送种子到下载器", description="""
推送种子到下载器。
""")
async def push_rss():
    RSS.Push()