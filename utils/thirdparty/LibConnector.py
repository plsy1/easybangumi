import subprocess
import os
from core.logs import *


def EpisodeReName_get_episode_name(name):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
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
