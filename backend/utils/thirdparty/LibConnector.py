import subprocess
import os
from core.logs import *


def EpisodeReName_get_episode_name(name):
    original_dir = os.getcwd()  # 保存原始工作目录
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)  # 切换到脚本所在目录
        result = subprocess.run(
            ["python", "EpisodeReName/EpisodeReName.py", name],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            output_str = result.stdout.strip()
            if output_str == name:
                return None
            return output_str
        else:
            LOG_ERROR("Error:", result.stderr)
            return None
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录