import os, subprocess
from pathlib import Path

import util
import project
import settings

class VcpkgInstance:
    root_path: Path = None
    
    def __init__(self, root_path):
        self.root_path = root_path
        
    @property
    def exec_path(self):
        platform = os.name
        if platform == 'nt':
            return self.root_path.joinpath("vcpkg.exe")
        else:
            return self.root_path.joinpath("vcpkg")
        
    @property
    def is_downloaded(self):
        return self.root_path.exists()
    
    @property
    def is_bootstrapped(self):
        return self.is_downloaded and self.exec_path.exists()
        