import sys, os, pathlib
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

    scb_user_dir = Path.home().joinpath(".scb")
    scb_user_settings_path = scb_user_dir.joinpath("scb_settings.json")

def make_path_str_forward_slashed(path_str: str) -> str:
    return path_str.replace('\\', '/')
