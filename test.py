from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from core.scheduler import Scheduler
from core.rss import RSS
from modules.database import DB
from modules.parse import *
from modules.bangumi import Bangumi_Helper

DB.download_status_delete_by_rss_single_id(1)


