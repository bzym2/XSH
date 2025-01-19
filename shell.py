#!/bin/python3

import json
import os
import platform
import subprocess
import sys
import shlex
import time
import hushExtLoader

registry = {}
startTime = int(time.time())
themeSet = 'personalize.colored_bash'
homePath = os.path.expanduser('~')

def changeDirectory(path: str):
    global _lastChangedWorkDir
    try:
        if path == '~':
            os.chdir(homePath)
            _lastChangedWorkDir = homePath
        else:
            os.chdir(path)
            _lastChangedWorkDir = path
    except FileNotFoundError:
        print(f"hush: cd: no such file or directory: {path}")
    except PermissionError:
        print(f"hush: cd: permission denied: {path}")

def processVariable(command: str):
    for i in registry:
        command = command.replace(f"${i}", registry[i])
    return command

def completer(text, state):
    global _lastCompleterList
    commands = os.listdir()
    if text:
        matches = []
        for cmd in commands:
            if cmd.lower().startswith(text.lower()):
                matches.append(cmd)

        custom_commands = ['_listvar', '_theme_list', '_theme_set', '_dump'
                           'cd', 'exit', 'quit', 'export', '_checkfile']
        for custom_cmd in custom_commands:
            if custom_cmd.lower().startswith(text.lower()):
                matches.append(custom_cmd)
    else:
        matches = commands

    _lastCompleterList = commands + custom_commands

    try:
        if matches:
            return matches[state]
        else:
            return None
    except IndexError:
        return None


def writeHistory(string):
    global hushLog
    with open(f"{homePath}/.hush_history", 'a+') as f:
        f.write(f'Session [{startTime}] at {time.ctime()}: {string}\n')
        hushLog.append(f'Session [{startTime}] at {time.ctime()}: {string}\n')

if platform.system() == 'Windows':
    print('Auto-completion has been disabled because this system is Windows.')
    pathChar = ';'
else:
    import readline
    pathChar = ':'
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

_lastChangedWorkDir = ''
_lastCompleterList = []
hushLog = []

def findExecutable(filename):
    if platform.system() == 'Windows':
        filename = filename + '.exe'
    for i in registry['PATH'].split(pathChar) + [os.getcwd()]:
        if os.path.exists(f'{i}/{filename}'):
            return f'{i}/{filename}'
    return False


def exit():
    writeHistory('Exiting...')
    sys.exit()

def _isSerializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

def main():
    global themeSet

    registry.update(os.environ)  # load system variable
    registry['SHELL'] = '/usr/bin/hush'
    
    
    hushExtLoader.Load()
    hushExtLoader.runPluginInit()

    try:
        writeHistory(f'A new session start by using {os.ttyname(0)}.')
    except AttributeError:
        writeHistory('A new session start by using cmd.')
    while True:
        hushExtLoader.runPluginPreHook()
        hushExtLoader.themeRefresh()
        theme = hushExtLoader.themes.get(themeSet, ' $')

        shinput = processVariable(input(theme))

        hushExtLoader.runPluginAfterHook()

        if not shinput:
            pass

        elif shinput == 'quit' or shinput == 'exit':
            exit()

        elif shinput.startswith('cd'):
            if shinput == 'cd':
                changeDirectory('~')
            else:
                path = shinput.split(' ', 1)[-1]
                changeDirectory(path)

        elif shinput == '_listvar':
            for i in registry:
                print(f"{i}: {registry[i]}")

        elif shinput.startswith('_theme_set'):
            themeSet = shinput.split(' ')[-1]

        elif shinput.startswith('_theme_list'):
            print("List of theme available:")
            for i in hushExtLoader.themes:
                print(f"\nTheme \"{i}\" preview:", end=f'\n{hushExtLoader.themes[i]}\n')

            print()

        elif shinput.startswith('_dump'):
            nowTime = int(time.time())
            _globalsFiltered = {}
            
            for key, value in globals().items():
                if _isSerializable(value):
                    _globalsFiltered[key] = value

            _globalsFiltered['systemType'] = platform.system()
            _globalsFiltered['systemVersion'] = platform.release()
            _globalsFiltered['systemArch'] = platform.machine()
            _globalsFiltered['pythonVersion'] = platform.python_version()
            _globalsFiltered['hushExtLoaderLog'] = hushExtLoader.Dump()
            
            print(f"Dumped to dump_{nowTime}_session{startTime}.json")
            with open(f"dump_{nowTime}_session{startTime}.json", "w") as f:
                json.dump(_globalsFiltered, f, indent=4, ensure_ascii=False)
        

        elif shinput.startswith('export '):
            parts = shinput.split(' ')

            registry[parts[1].split('=')[0]] = parts[1].split('=')[1].strip()
        elif shinput.startswith('_checkfile '):
            print(findExecutable(shinput.split(' ')[1]))
        else:
            parts = shlex.split(shinput)
            flag = findExecutable(parts[0])

            if flag:
                try:
                    processReturn = subprocess.run(
                        parts, env=registry, shell=False)
                    writeHistory(
                        f"Executed \"{shinput}\", return code: {processReturn.returncode}.")
                except Exception as f:
                    print(f"hush: {f}")
                    writeHistory(
                        f"Executed \"{shinput}\", return code: {processReturn.returncode}.")
            else:
                print(f"hush: {parts[0]}: not found")
                writeHistory(
                    f"Executed \"{shinput}\", but this command is not found.")

            # subprocess.run(shinput, env=registery, shell=True)


while True:
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye")
        exit()
