import os, shutil, json, subprocess
from typing import Union

import util
import settings

current = None

def default_project_config():
    return {
        "name": "my_project",
        "version": "1.0.0",
        "description": "description of project",
        "authors": [
            "Author 1"
        ],
        "vcpkg": {
            "repo_uri": "https://github.com/microsoft/vcpkg.git",
            "disable_metrics": True,
            "local_path": "./vcpkg",
            "packages": []
        }
        
    }

def load_project_file(filePath: str):
    global current
    
    current = default_project_config()
    util.load_json_config(filePath, current)


def save_project_file(filePath: str):
    global current
    util.save_json_config(filePath, current)
    