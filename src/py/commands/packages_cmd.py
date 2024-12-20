from re import sub
from typing import Union

import sys, os, subprocess, argparse, shutil, json
from pathlib import Path


from util import *
from colors import *
import project
import settings


from tools import vcpkg, cmake_presets

from commands import CommandBase

default_pkglists_filename = "vcpkg-lists.json"

class VcpkgCommand(CommandBase):
    cmd: str = "vcpkg"
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Run 'vcpkg' tool directly."
    )
    parse: bool = False

    def setup_args(self):
        pass

    def process(self, args: argparse.Namespace):
        
        if not project.info.vcpkg.is_bootstrapped:
            print_error("ERROR: Vcpkg is not set up... ")
            return 1
        
        params = sys.argv[2:]      
        
        result = subprocess.run([project.info.vcpkg.exec_path] + params, cwd=project.info.vcpkg.root_path)

        if result.returncode != 0:
            return result
