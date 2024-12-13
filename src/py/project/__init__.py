import os, shutil, json, subprocess
from typing import Union
from pathlib import Path

import util

config_file_name = "scb_project_config.json"
current_config_path: Path = None
current_config: dict = None

def is_project_found() -> bool:
    return current_config_path is not None

def get_project_root() -> Path:
    global current_config_path

    if is_project_found():
        return current_config_path.parent
    return None

def default_project_config():
    return {
        "name": "my_project",
        "version": "1.0.0",
        "description": "description of project",
        "authors": [
            "Author 1"
        ],
        "vcpkg": {
            "local_path": "./vcpkg",
            "packages": []
        }
    }

def attempt_load_project():
    global config_file_name, current_config_path, current_config
    
    current_config_path = locate_project_file()
    if current_config_path != None:
        util.print_color("green", f"-> Running for local project '{get_project_root()}':")
        load_project_config(current_config_path)
    else:
        print("green", "-> Running globally: ")
        
        
def locate_project_file() -> Path:
    global config_file_name
    
    # Recurse up the current directory tree to find the current project file.
    search_dir = Path.cwd()
    while True:
        for candidate in [search_dir.joinpath(i) for i in os.listdir(search_dir)]:
            if not candidate.is_file() or candidate.name != config_file_name:
                continue
            
            return candidate
        
        if len(search_dir.parents) == 0:
            break
        search_dir = search_dir.parent
        
    return None

def load_project_config(filePath: str = current_config_path):
    global current_config
    
    current_config = default_project_config()
    util.load_json_config(filePath, current_config)


def save_project_config(filePath: str = current_config_path):
    global current_config
    util.save_json_config(filePath, current_config)
    