#!/bin/python3
import os
import getpass
import platform
import platform
import readline # keyboard support
import subprocess
import globalvars
import colorama

if platform.system == 'Windows':
    path_char = ';'
else:
    path_char = ':'

colorama.init()

print(globalvars.logo_colossal)
print(globalvars.logo_text)

registry = {}

style = {}

def getPrefix(theme: str = ''):
    global style
    style = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# ",
        'kali': f"{colorama.Fore.BLUE}┌──({getpass.getuser()}㉿{colorama.Fore.RED}kali{colorama.Fore.BLUE})-[{os.getcwd().replace(os.path.expanduser('~'), '~')}]\n└──{colorama.Fore.RESET}$ ",
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
        
        custom_commands = ['_listvar', '_theme_list', '_theme_set', 'cd', 'exit', 'quit', 'export', '_checkfile']
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

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def findExecutable(filename):
    for i in registry['PATH'].split(path_char) + [os.getcwd()]:
        if os.path.exists(f'{i}/{filename}'):
            return f'{i}/{filename}'
    return False

def main():
    theme = "bash"

    registry.update(os.environ) # load system variable
    registry['SHELL'] = '/usr/bin/hush'
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
            print("List of theme available:\n")
            for i in style:
                print(f"Theme \"{i}\" preview:", end=f'\n{style[i]}\n')

            print()
    
        elif shinput.startswith('export '):
            parts = shinput.split(' ')

            registry[parts[1].split('=')[0]] = parts[1].split('=')[1].strip()
        elif shinput.startswith('_checkfile '):
            print(findExecutable(shinput.split(' ')[1]))
        else:
            parts = shinput.split(' ')
            flag = findExecutable(parts[0])

            if flag:
                try:
                    subprocess.run(parts, env=registry, shell=False)
                except Exception as f:
                    print(f"hush: {f}")
            else:
                print("hush: File do not exists, please check your command and try again.")
                
            # subprocess.run(shinput, env=registery, shell=True)
                


while True:
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye")
        exit(0)
