import sys, os, json
from pathlib import Path

from colors import *
import util
from . import paths
# If we're executing as the source version, the main .py file  is actually found in the `src` subdirectory
# of the project, and `exec_dir` is changed to reflect that. We'll create `exec_file_dir` in case we actually need the
# unmodified path to that script. Obviously, in build mode, these two values will be the same.

def default_settings():
    return {
        "common": {
            "additional_template_dirs": []
        },
        "vcpkg": {
            "repo_uri": "https://github.com/microsoft/vcpkg.git",
            "disable_metrics": True,
        },
    }

current = default_settings()

def save_settings(path: str = paths.scb_user_settings_path, settings_dict: dict = current):
    util.save_json_config(path, settings_dict)


def load_settings(path: Path = paths.scb_user_settings_path, settings_dict: dict = current):
    util.load_json_config(path, settings_dict)

