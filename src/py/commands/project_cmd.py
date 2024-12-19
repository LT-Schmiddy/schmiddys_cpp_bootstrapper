from re import sub
from typing import Union

import sys, os, subprocess, argparse, json

from util import *
from colors import *
import project
import settings

from commands import CommandBase

class SetupProjectCommand(CommandBase):
    cmd: str = "init"
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Setup a SCB project and CMake preset files."
    )

    def setup_args(self):
        self.argparser.add_argument(
            "-p",
            "--path",
            default=os.getcwd()
        )

        self.argparser.add_argument(
            "-f",
            "--force",
            action='store_true'
        )

    def process(self, args: argparse.Namespace):
        mkdir_if_missing(args.path)
        
        

        

class AddTripletCommand(CommandBase):
    standard_build_types: list[str] = [
        "Debug",
        "Release",
        "RelWithDebInfo",
        "MinSizeRel",
    ]
    
    cmd: str = "add-triplet"
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds presets for a vcpkg triplet"
    )

    def setup_args(self):
        self.argparser.add_argument('triplet')
        config_group = self.argparser.add_argument_group()
        config_group.add_argument(
            '-b',
            "--build_type",
            default=""
        )
        
        config_group.add_argument(
            '-a',
            "--all_build_types",
            action='store_true'
        )

    def process(self, args: argparse.Namespace):
        pass
