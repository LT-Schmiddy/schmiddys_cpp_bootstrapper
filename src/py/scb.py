import sys, os, argparse

from colors import *
from util import *

import settings
import project
import commands

    
def init_user():
    settings.paths.init_paths()
    
    if mkdir_if_missing(settings.paths.scb_user_dir):
        print(f"Created scb user directory at '{settings.paths.scb_user_dir}'.")
        
    settings.load_settings(settings.paths.scb_user_settings_path)


def print_cmd_list():
    for cmd, desc in commands.get_command_desc().items():
        print(f"\t{cmd} - {desc}")
    print(
        f"\tg[lobal] ... - Ignore local project and run following command globally (if applicable)."
    )


def args_len_check():
    if len(sys.argv) < 2:
        print_error("FATAL ERROR: No command given. Valid commands are:")
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

    # if settings.s_globals["vcpkg"]["path"] is None:
    #     print_warning("WARNING: global vcpkg installation unset.")
    #     print_warning(
    #         f"Before you can use MCT properly, you must run either 'mct g install-vcpkg' to install a global "\
    #             f"vcpkg instance, or set the path to one manually in '{settings.settings_path}'."
    #     )
    #     print_warning(
    #         "If that is what you're currently trying to do, then you may disregard this message."
    #     )

    # if settings.is_local_project:
    #     print("-> Running for local project: '" + settings.project_dir + "': ")
    # else:
    #     print("-> Running globally: ")

    cmd = sys.argv[1]
    cmds = commands.get_commands()

    # if command is not valid:
    if cmd not in cmds:
        print_error(f"FATAL ERROR '{cmd}' is not a valid command. Valid commands are:")
        print_cmd_list()
        sys.exit(1)

    # Initialize and execute command:
    cmd_runner = cmds[cmd]()
    result = cmd_runner.run(sys.argv[2:])

    if result is None:
        print_color("green", "Command completed successfully!")

        if settings.is_local_project:
            settings.save_settings(settings.local_settings_path, settings.current)
        else:
            settings.save_settings(settings.settings_path, settings.current)

        sys.exit(0)

    elif isinstance(result, str):
        print_error(f"FATAL ERROR: {result}")
        sys.exit(1)

    elif isinstance(result, int):
        print_error(f"FATAL ERROR: Error code {result}")
        sys.exit(result)

    else:
        print_error(f"FATAL ERROR: Unknown cause - {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()