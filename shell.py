#!/bin/python3

from colorama import init, Fore, Style
import os
import getpass
import platform
import subprocess
import sys
import globalvars
import shlex
import time

init(autoreset=True)

print(globalvars.logo_roman)
print(globalvars.motd)

registry = {}
style = {}
startTime = int(time.time())
theme = "colored_bash"


def getPrefix(theme: str = ''):
    global style
    style = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# ",
        'colored_bash': f"{Style.BRIGHT}{Fore.GREEN}{getpass.getuser()}@{platform.node()}{Fore.BLUE}:{os.getcwd().replace(os.path.expanduser('~'), '~')}{Style.RESET_ALL}$ ",
        'fish': f"{Fore.LIGHTGREEN_EX}{getpass.getuser()}{Style.RESET_ALL}@{platform.node()} {Fore.RED}{os.getcwd().replace(os.path.expanduser('~'), '~')}{Style.RESET_ALL}# ",
        'kali': f"{Fore.BLUE}┌──({getpass.getuser()}㉿{Fore.RED}kali{Fore.BLUE})-[{os.getcwd().replace(os.path.expanduser('~'), '~')}]\n└──{Fore.RESET}$ ",
        'hush': f"╭─[{getpass.getuser()} on Hush]\n╰─{os.getcwd().replace(os.path.expanduser('~'), '~')}> ",
        'omega': f"╭──(ø@{getpass.getuser()})\n╰──{os.getcwd().replace(os.path.expanduser('~'), '~')}> "
    }
    return style.get(theme, '$ ')


def change_directory(path: str):
    try:
        if path == '~':
            os.chdir(os.path.expanduser('~'))
        else:
            os.chdir(path)
    except FileNotFoundError:
        print(f"hush: cd: no such file or directory: {path}")
    except PermissionError:
        print(f"hush: cd: permission denied: {path}")


def processVariable(command: str):
    for i in registry:
        command = command.replace(f"${i}", registry[i])
    return command


def completer(text, state):
    commands = os.listdir()
    if text:
        matches = []
        for cmd in commands:
            if cmd.lower().startswith(text.lower()):
                matches.append(cmd)

        custom_commands = ['_listvar', '_theme_list', '_theme_set',
                           'cd', 'exit', 'quit', 'export', '_checkfile']
        for custom_cmd in custom_commands:
            if custom_cmd.lower().startswith(text.lower()):
                matches.append(custom_cmd)
    else:
        matches = commands

    try:
        if matches:
            return matches[state]
        else:
            return None
    except IndexError:
        return None


def writeHistory(string):
    with open(f"{os.path.expanduser('~')}/.hush_history", 'a+') as f:
        f.write(f'Session [{startTime}] at {time.ctime()}: {string}\n')


if platform.system() == 'Windows':
    print('Auto-completion has been disabled because this system is Windows.')
    path_char = ';'
else:
    import readline
    path_char = ':'
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")


def findExecutable(filename):
    if platform.system() == 'Windows':
        filename = filename + '.exe'
    for i in registry['PATH'].split(path_char) + [os.getcwd()]:
        if os.path.exists(f'{i}/{filename}'):
            return f'{i}/{filename}'
    return False


def exit():
    writeHistory('Exiting...')
    sys.exit()


def main():
    global style, theme

    registry.update(os.environ)  # load system variable
    registry['SHELL'] = '/usr/bin/hush'
    try:
        writeHistory(f'A new session start by using {os.ttyname(0)}.')
    except AttributeError:
        writeHistory('A new session start by using cmd.')
    while True:
        shinput = processVariable(input(getPrefix(theme)))

        if not shinput:
            pass

        elif shinput == 'quit' or shinput == 'exit':
            exit()

        elif shinput.startswith('cd'):
            if shinput == 'cd':
                change_directory('~')
            else:
                path = shinput.split(' ', 1)[-1]
                change_directory(path)

        elif shinput == '_listvar':
            for i in registry:
                print(f"{i}: {registry[i]}")

        elif shinput.startswith('_theme_set'):
            theme = shinput.split(' ')[-1]

        elif shinput.startswith('_theme_list'):
            print("List of theme available:")
            for i in style:
                print(f"\nTheme \"{i}\" preview:", end=f'\n{style[i]}\n')

            print()

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
