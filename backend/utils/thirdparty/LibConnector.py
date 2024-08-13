import subprocess
import os
from core.logs import *



def EpisodeReName_get_episode_name(name):
    try:
        result = subprocess.run(
            ["python3", "utils/thirdparty/EpisodeReName/EpisodeReName.py", name],
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
    except Exception as e:
        LOG_ERROR("EpisodeReName_get_episode_name",e)