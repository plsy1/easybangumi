from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from core.scheduler import Scheduler
from core.rss import RSS
from modules.database import DB

@asynccontextmanager
async def lifespan(App: FastAPI):
    init_routers()
    DB.create_table()
    RSS.Init()
    Scheduler.run_scheduler()
    yield
    
    
App = FastAPI(lifespan=lifespan)

App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Config = uvicorn.Config(App, host="0.0.0.0", port=18964, log_level="info", reload=True,)

Server = uvicorn.Server(Config)


def init_routers():
    from api.api import api_router
    App.include_router(api_router, prefix="/api/v1")
    
        
if __name__ == '__main__':
    Server.run()