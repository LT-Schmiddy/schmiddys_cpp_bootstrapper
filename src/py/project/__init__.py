import os, shutil, json, subprocess
from typing import Union
from pathlib import Path

import util

class ProjectInfo:
    config_file_name = "scb_project_config.json"
    current_config_path: Path = None
    current_config: dict = None
    
    @classmethod
    def default_project_config(cls):
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
    
    def __init__(self, current_path: Path = None):
        pass
    
    def is_project(self) -> bool:
        return self.current_config_path is not None

    def get_project_root(self) -> Path:
        if self.is_project():
            return self.current_config_path.parent
        return None
    
    
    def attempt_load_project(self, current_path: Path = None):
        if current_path is None:
            current_path = Path(os.cwd())
        
        self.current_config_path = self.locate_project_file()
        if self.current_config_path  is not None:
            self.load_project_config(self.current_config_path)
            
    def locate_project_file(self, current_path: Path = None) -> Path:
        if current_path is None:
            current_path = Path(os.cwd())
        
        # Recurse up the current directory tree to find the current project file.
        search_dir = current_path;
        while True:
            for candidate in [search_dir.joinpath(i) for i in os.listdir(search_dir)]:
                if not candidate.is_file() or candidate.name !=self.config_file_name:
                    continue
                
                return candidate
            
            if len(search_dir.parents) == 0:
                break
            search_dir = search_dir.parent
            
        return None
    
    
    def load_project_config(self, file_path: Path = None):
        if file_path is None:
            file_path = self.current_config_path
        
        self.current_config = self.default_project_config()
        util.load_json_config(file_path, self.current_config)


    def save_project_config(self, file_path: Path = None):
        if file_path is None:
            file_path = self.current_config_path
            
        util.save_json_config(file_path, self.current_config)
        
info = ProjectInfo()
