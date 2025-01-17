#!/bin/python3

import os
import getpass
import platform
import readline # keyboard support
import subprocess
import globalvars

theme = "bash"
registery = {}

registery.update(os.environ) # load system variable
registery['SHELL'] = '/usr/bin/hush'

print(globalvars.logo)
print(globalvars.logo_text)

def getPrefix(theme: str = ''):
    style = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# ",
        'kali': f"┌──({getpass.getuser()}㉿kali)-[~{os.getcwd().replace(os.path.expanduser('~'), '~')}]\n└──$ "
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
    for i in registery:
        command = command.replace(f"${i}", registery[i])
    return command

def main():
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
            for i in registery:
                print(f"{i}: {registery[i]}")
    
        elif shinput.startswith('export '):
            parts = shinput.split(' ')

            registery[parts[1].split('=')[0]] = parts[1].split('=')[1].strip()

        else:
            subprocess.run(shinput, env=registery, shell=True)


try:
    main()
except Exception as f:
    print(f)
    exit()
