import sys, os, pathlib, json
from typing import Union
from pathlib import Path

import util

exec_path: Path = None
exec_dir: Path = None

scb_user_dir: Path = None
scb_user_settings_path: Path = None

def init_paths():
    global exec_path, exec_dir, scb_user_dir, scb_user_settings_path
    exec_path = Path(os.path.abspath(sys.argv[0]))
    exec_dir = exec_path.parent
    
    # Useful for development: set a custom path for the user home from a text file
    dev_paths = {}
    dev_paths_file = exec_dir.joinpath("dev_paths.json")
    if dev_paths_file.exists():
        dev_paths = json.loads(dev_paths_file.read_text())

    if "custom_user_path" in dev_paths:
        custom_user_path = Path(dev_paths["custom_user_path"])
        
        if not custom_user_path.is_absolute():
            custom_user_path = exec_dir.joinpath(dev_paths["custom_user_path"])
        
        scb_user_dir = custom_user_path
        print(f"DEV: using custom user path '{custom_user_path}'")
    else:
        scb_user_dir = Path.home().joinpath(".scb")
    scb_user_settings_path = scb_user_dir.joinpath("scb_settings.json")

def make_path_str_forward_slashed(path_str: str) -> str:
    return path_str.replace('\\', '/')
