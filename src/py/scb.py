import sys, os, argparse

from colors import *
import util

import settings
import project
import commands

    
def init_user():
    settings.paths.init_paths()
    
    if util.mkdir_if_missing(settings.paths.scb_user_dir):
        print(f"Created scb user directory at '{settings.paths.scb_user_dir}'.")
        
    settings.load_settings()


def print_cmd_list():
    for cmd, desc in commands.get_command_desc().items():
        print(f"\t{cmd} - {desc}")
    print(
        f"\tg[lobal] ... - Ignore local project and run following command globally (if applicable)."
    )


def args_len_check():
    if len(sys.argv) < 2:
        util.print_error("FATAL ERROR: No command given. Valid commands are:")
        print_cmd_list()

        sys.exit(1)


def main():
    init_user()

    # if no command is given:
    args_len_check()
    # Force global check:
    if sys.argv[1] in ["g", "global"]:
        del sys.argv[1]
        # We've edited the args list. Need to check length again:
        # print("-> (Forced) Running globally: ")
        args_len_check()
    else:
        project.info.attempt_load_project()
        
    if project.info.is_project():
        util.print_color("green", f"-> Running for local project '{project.info.get_project_root()}':")
    else:
        util.print_color("green", "-> Running without project: ")

    cmd = sys.argv[1]
    cmds = commands.get_commands()

    # if command is not valid:
    if cmd not in cmds:
        util.print_error(f"FATAL ERROR '{cmd}' is not a valid command. Valid commands are:")
        print_cmd_list()
        sys.exit(1)

    # Initialize and execute command:
    cmd_runner = cmds[cmd]()
    result = cmd_runner.run(sys.argv[2:])

    if result is None:
        util.print_color("green", "Command completed successfully!")
        settings.save_settings()
        sys.exit(0)

    elif isinstance(result, str):
        util.print_error(f"FATAL ERROR: {result}")
        sys.exit(1)

    elif isinstance(result, int):
        util.print_error(f"FATAL ERROR: Error code {result}")
        sys.exit(result)

    else:
        util.print_error(f"FATAL ERROR: Unknown cause - {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()