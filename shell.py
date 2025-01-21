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
startTime = time.time()
startTime_formatted = time.ctime()
themeSet = DEFAULT_THEME
homePath = os.path.expanduser("~")
last_changed_work_dir = ''
last_completer_list = []
hushLog = []
pathChar = ':'

enableCompleter = False

if platform.system() == WINDOWS_PLATFORM:
    pathChar = ';'
    print("Auto-completion has been disabled because this system is Windows.")
else:
    enableCompleter = True


def changeDirectory(path: str):
    """Changes the current working directory."""
    global last_changed_work_dir
    try:
        targetPath = homePath if path == "~" else path
        os.chdir(targetPath)
        last_changed_work_dir = targetPath
    except FileNotFoundError:
        print(f"hush: cd: no such file or directory: {path}")
    except PermissionError:
        print(f"hush: cd: permission denied: {path}")


def processVariable(command: str):
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

        customCommands = [
            '_list_plugins',
            '_list_var',
            '_theme_list', 
            '_theme_set', 
            '_checkfile',
            '_dump',               
            'cd', 
            'exit', 
            'quit', 
            'export', 
        ]
        for customCommand in customCommands:
            if customCommand.lower().startswith(text.lower()):
                matches.append(customCommand)

        for pluginCommand in hushExtLoader.registeredCommands:
            if pluginCommand.lower().startswith(text.lower()):
                matches.append(pluginCommand)
    else:
        matches = commands

    last_completer_list = matches 
    try:
        return matches[state] if matches else None
    except IndexError:
        return None


def writeHistory(string):
    """Appends a command to the history file and in-memory log."""
    timestamp = int(startTime)
    formattedTime = time.ctime()
    history_entry = f"Session [{timestamp}] at {formattedTime}: {string}\n"
    with open(HISTORY_FILE, "a+") as f:
        f.write(history_entry)
    hushLog.append(history_entry)


def findExecutable(filename):
    """Finds the full path to an executable file."""
    if platform.system() == WINDOWS_PLATFORM:
        filename += ".exe"
    searchPaths = registry.get('PATH', '').split(pathChar) + [os.getcwd()]
    for path in searchPaths:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    return False


def exit():
    """Exits the shell."""
    writeHistory("Exiting...")
    sys.exit()


def isSerializable(obj):
    """Checks if an object can be serialized to JSON."""
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def main():
    """Main shell loop."""
    global themeSet, startTime_formatted
    registry.update(os.environ)  # load system variable
    registry['SHELL'] = '/usr/bin/hush'

    hushExtLoader.Load()
    hushExtLoader.runPluginInit()

    try:
        writeHistory(f"A new session start by using {os.ttyname(0)}.")
    except AttributeError:
        writeHistory("A new session start by using cmd.")

    while True:
        hushExtLoader.runPluginPreHook()
        hushExtLoader.themeRefresh()
        theme = hushExtLoader.themes.get(themeSet, " $")

        try:
            shinput = processVariable(input(theme))
            args = shlex.split(shinput)
        except EOFError:
            print()
            exit()

        hushExtLoader.runPluginAfterHook()

        if not shinput:
            continue

        pluginCommand = hushExtLoader.registeredCommands.get(args[0], None) 
        executablePath = findExecutable(args[0])


        if pluginCommand:
            pluginCommand(args)

        elif shinput in ("quit", "exit"):
            exit()

        elif shinput.startswith("cd"):
            targetPath = shinput.split(" ", 1)[-1] if " " in shinput else "~"
            changeDirectory(targetPath) 

        elif shinput.startswith("_set_theme"):
            themeSet = shinput.split(" ")[-1]

        elif shinput == "_list_var":
            for key, value in registry.items():
                print(f"{key}: {value}")

        elif shinput == "_list_plugins":
            for plugin in hushExtLoader.loadedPlugins:
                print(plugin)

        elif shinput.startswith("_list_theme"):
            print("List of theme available:")
            for Name, Preview in hushExtLoader.themes.items():
                print(f'\nTheme "{Name}" preview:\n{Preview}\n')

        elif shinput.startswith("_dump"):
            nowTime = time.time()
            globals_filtered = {
                key: value for key, value in globals().items() if isSerializable(value)
            }
            globals_filtered.update({
                'systemType': platform.system(),
                'systemVersion': platform.release(),
                'systemArch': platform.machine(),
                'pythonVersion': platform.python_version(),
                'dumpTime': nowTime,
                'dumpTimeFormated': time.ctime(),
                'hushExtLoaderLog': hushExtLoader.Dump()
            })

            filename = f"dump_{int(nowTime)}.json"
            print(f"Dumped to {filename}")
            with open(filename, "w") as f:
                json.dump(globals_filtered, f, indent=4, ensure_ascii=False)

        elif shinput.startswith("export"):
            args = shlex.split(shinput)
            if len(args) > 1 and "=" in args[1]:
                key, value = args[1].split("=", 1)
                registry[key] = value.strip()
            else:
                for i in registry:
                    print(f'{i}={registry[i]}')

        elif shinput.startswith("_checkfile "):
            filename = shinput.split(" ")[1]
            print(findExecutable(filename))

        elif executablePath:
            try:
                process_return = subprocess.run(
                    args, env=registry, shell=False)
                writeHistory(
                    f'Executed "{shinput}", return code: {process_return.returncode}.')
                if process_return.stderr:
                    print(f"Error: {process_return.stderr}")
            except Exception as e:
                print(f"hush: {e}")
                writeHistory(f'Executed "{shinput}", but an error occurred: {e}.')
        else:
            print(f"hush: {args[0]}: not found")
            writeHistory(f'Executed "{shinput}", but this command is not found.')


while True:
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye")
        exit()
