#!/usr/bin/env python3

import json
import os
import platform
import subprocess
import sys
import shlex
import time
import readline
import hushExtLoader

# Constants
HISTORY_FILE = os.path.expanduser("~/.hush_history")
DEFAULT_THEME = "personalize.colored_bash"
WINDOWS_PLATFORM = "Windows"

# Global Variables
registry = {}
start_time = time.time()
start_time_formatted = time.ctime()
theme_set = DEFAULT_THEME
home_path = os.path.expanduser("~")
last_changed_work_dir = ''
last_completer_list = []
hush_log = []
path_char = ':'
if platform.system() == WINDOWS_PLATFORM:
    path_char = ';'
    print("Auto-completion has been disabled because this system is Windows.")
else:
    readline.set_completer(lambda text, state: completer(text, state))
    readline.parse_and_bind("tab: complete")


def change_directory(path: str):
    """Changes the current working directory."""
    global last_changed_work_dir
    try:
        target_path = home_path if path == "~" else path
        os.chdir(target_path)
        last_changed_work_dir = target_path
    except FileNotFoundError:
        print(f"hush: cd: no such file or directory: {path}")
    except PermissionError:
        print(f"hush: cd: permission denied: {path}")


def process_variable(command: str):
    """Replaces variables in a command string with their values from the registry."""
    for key, value in registry.items():
        command = command.replace(f"${key}", value)
    return command


def completer(text, state):
    """Provides tab-completion suggestions."""
    global last_completer_list
    commands = os.listdir()
    matches = []

    if text:
        for cmd in commands:
            if cmd.lower().startswith(text.lower()):
                matches.append(cmd)

        custom_commands = ['_listvar', '_theme_list', '_theme_set', '_dump',
                           'cd', 'exit', 'quit', 'export', '_checkfile']
        for custom_cmd in custom_commands:
            if custom_cmd.lower().startswith(text.lower()):
                matches.append(custom_cmd)

        for plugin_cmd in hushExtLoader.registeredCommands:
            if plugin_cmd.lower().startswith(text.lower()):
                matches.append(plugin_cmd)
    else:
        matches = commands

    last_completer_list = commands + custom_commands
    try:
        return matches[state] if matches else None
    except IndexError:
        return None


def write_history(string):
    """Appends a command to the history file and in-memory log."""
    timestamp = int(start_time)
    formatted_time = time.ctime()
    history_entry = f"Session [{timestamp}] at {formatted_time}: {string}\n"
    with open(HISTORY_FILE, "a+") as f:
        f.write(history_entry)
    hush_log.append(history_entry)


def find_executable(filename):
    """Finds the full path to an executable file."""
    if platform.system() == WINDOWS_PLATFORM:
        filename += ".exe"
    search_paths = registry.get('PATH', '').split(path_char) + [os.getcwd()]
    for path in search_paths:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    return False


def exit_shell():
    """Exits the shell."""
    write_history("Exiting...")
    sys.exit()


def is_serializable(obj):
    """Checks if an object can be serialized to JSON."""
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


def main():
    """Main shell loop."""
    global theme_set, start_time_formatted
    registry.update(os.environ)  # load system variable
    registry['SHELL'] = '/usr/bin/hush'

    hushExtLoader.load()
    hushExtLoader.run_plugin_init()

    try:
        write_history(f"A new session start by using {os.ttyname(0)}.")
    except AttributeError:
        write_history("A new session start by using cmd.")

    while True:
        hushExtLoader.run_plugin_pre_hook()
        hushExtLoader.theme_refresh()
        theme = hushExtLoader.themes.get(theme_set, " $")

        try:
            shinput = process_variable(input(theme))
            args = shlex.split(shinput)
        except EOFError:
            print()
            exit_shell()

        hushExtLoader.run_plugin_after_hook()
        plugin_command = hushExtLoader.registeredCommands.get(args[0], None) if args else None

        if not shinput:
            continue

        if plugin_command:
            plugin_command(args)
            continue

        if shinput in ("quit", "exit"):
            exit_shell()

        if shinput.startswith("cd"):
            target_path = shinput.split(" ", 1)[-1] if " " in shinput else "~"
            change_directory(target_path)
            continue

        if shinput == "_listvar":
            for key, value in registry.items():
                print(f"{key}: {value}")
            continue

        if shinput.startswith("_theme_set"):
            theme_set = shinput.split(" ")[-1]
            continue

        if shinput.startswith("_theme_list"):
            print("List of theme available:")
            for theme_name, theme_preview in hushExtLoader.themes.items():
                print(f'\nTheme "{theme_name}" preview:\n{theme_preview}\n')
            continue

        if shinput.startswith("_dump"):
            now_time = time.time()
            globals_filtered = {
                key: value for key, value in globals().items() if is_serializable(value)
            }
            globals_filtered.update({
                'systemType': platform.system(),
                'systemVersion': platform.release(),
                'systemArch': platform.machine(),
                'pythonVersion': platform.python_version(),
                'dumpTime': now_time,
                'dumpTimeFormated': time.ctime(),
                'hushExtLoaderLog': hushExtLoader.dump()
            })

            filename = f"dump_{int(now_time)}.json"
            print(f"Dumped to {filename}")
            with open(filename, "w") as f:
                json.dump(globals_filtered, f, indent=4, ensure_ascii=False)
            continue

        if shinput.startswith("export "):
            parts = shinput.split(" ")
            if len(parts) >= 2 and "=" in parts[1]:
                key, value = parts[1].split("=", 1)
                registry[key] = value.strip()
            continue

        if shinput.startswith("_checkfile "):
            filename = shinput.split(" ")[1]
            print(find_executable(filename))
            continue

        parts = shlex.split(shinput)
        executable_path = find_executable(parts[0])

        if executable_path:
            try:
                process_return = subprocess.run(
                    parts, env=registry, shell=False, capture_output=True, text=True)
                write_history(
                    f'Executed "{shinput}", return code: {process_return.returncode}.')
                if process_return.stderr:
                    print(f"Error: {process_return.stderr}")
            except Exception as e:
                print(f"hush: {e}")
                write_history(f'Executed "{shinput}", but an error occurred: {e}.')
        else:
            print(f"hush: {parts[0]}: not found")
            write_history(f'Executed "{shinput}", but this command is not found.')


while True:
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye")
        exit_shell()
