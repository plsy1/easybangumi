import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import os, sys

log_dir = "logs"

if getattr(sys, "frozen", False):  # 检查是否是打包后的运行环境

    project_root = os.path.dirname(sys.argv[0])
    print(f"Running in frozen environment. Config file path: {project_root}")

else:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

log_dir_path = os.path.join(project_root, log_dir)

if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

log_file = os.path.join(log_dir_path, 'backend.log')

file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)


error_file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(log_formatter)

# 控制台输出
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

# Logger配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(error_file_handler)


def LOG_ERROR(text, e=None):
    if not e == None:
        logger.error(f"Error Info: {text} {e}")
    else:
        logger.error(f"Error Info: {text} ")


def LOG_INFO(text,e=None):
    if not e == None:
        logger.info(f"Background Info: {text} {e}")
    else:
        logger.info(f"Background Info: {text} ")
