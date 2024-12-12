import sys, os, json
from pathlib import Path

from colors import *
import util
from . import paths
# If we're executing as the source version, the main .py file  is actually found in the `src` subdirectory
# of the project, and `exec_dir` is changed to reflect that. We'll create `exec_file_dir` in case we actually need the
# unmodified path to that script. Obviously, in build mode, these two values will be the same.

def default_settings():
    return {
        "common": {
            "additional_template_dirs": []
        },
        "vcpkg": {
            "repo_uri": "https://github.com/microsoft/vcpkg.git",
            "disable_metrics": True,
        },
    }

current = default_settings()

def load_settings(path: Path = paths.scb_user_settings_path, settings_dict: dict = current):

    def recursive_load_list(main: list, loaded: list):
        for i in range(0, max(len(main), len(loaded))):
            # Found in both:
            if i < len(main) and i < len(loaded):
                if isinstance(loaded[i], dict):
                    recursive_load_dict(main[i], loaded[i])
                elif isinstance(loaded[i], list):
                    recursive_load_list(main[i], loaded[i])
                else:
                    main[i] = loaded[i]
            # Found in main only:
            elif i < len(loaded):
                main.append(loaded[i])


    def recursive_load_dict(main: dict, loaded: dict):
        new_update_dict = {}
        for key, value in main.items():
            if not (key in loaded):
                continue
            if isinstance(value, dict):
                recursive_load_dict(value, loaded[key])
            elif isinstance(value, list):
                recursive_load_list(value, loaded[key])
            else:
                new_update_dict[key] = loaded[key]
        
        # Load settings added to file:
        for key, value in loaded.items():
            if not (key in main):
                new_update_dict[key] = loaded[key]

        main.update(new_update_dict)

    # load preexistent settings file
    if path.exists() and path.is_file():
        try:
            imported_settings = json.load(open(path, "r"))
            # current.update(imported_settings)
            recursive_load_dict(settings_dict, imported_settings)
        except json.decoder.JSONDecodeError as e:
            util.print_error(f"CRITICAL ERROR IN LOADING SETTINGS: {e}")
            util.print_error("Using default settings...", fg='yellow')

    # settings file not found
    else:
        save_settings(path, settings_dict)
        print(f"Created new settings file at '{path}'.")


def save_settings(path: str = paths.scb_user_settings_path, settings_dict: dict = current):
    outfile = open(path, "w")
    json.dump(settings_dict, outfile, indent=4)
    outfile.close()

