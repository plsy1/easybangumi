from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from core.scheduler import Scheduler
from core.rss import RSS
from modules.database import DB

def init():
    DB.Init()
    RSS.Init()
    Scheduler.Start()
    initRouter()



@asynccontextmanager
async def lifespan(App: FastAPI):
    init()
    yield
    
    
App = FastAPI(lifespan=lifespan)

App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Config = uvicorn.Config(App, host="0.0.0.0", port=8964, log_level="info", reload=False,)

Server = uvicorn.Server(Config)


def initRouter():
    from api.api import api_router
    App.include_router(api_router, prefix="/api/v1")
    
        
if __name__ == '__main__':
    Server.run()