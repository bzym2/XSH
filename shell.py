#!/bin/python3
import os
import getpass
import platform
import readline # keyboard support
import subprocess
import globalvars

print(globalvars.logo)
print(globalvars.logo_text)

registery = {}

def getPrefix(theme: str = ''):
    style = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# ",
        'kali': f"┌──({getpass.getuser()}㉿kali)-[{os.getcwd().replace(os.path.expanduser('~'), '~')}]\n└──$ ",
        'hush': f"┌──[{getpass.getuser()} on daSH]\n└──{os.getcwd().replace(os.path.expanduser('~'), '~')}> ",
        'omega': f"┌──(ø@{getpass.getuser()})\n└──{os.getcwd().replace(os.path.expanduser('~'), '~')}> "
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
    theme = "bash"

    registery.update(os.environ) # load system variable
    registery['SHELL'] = '/usr/bin/hush'
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

        elif shinput.startswith('_themechanger'):
            theme = shinput.split(' ')[-1]
    
        elif shinput.startswith('export '):
            parts = shinput.split(' ')

            registery[parts[1].split('=')[0]] = parts[1].split('=')[1].strip()

        else:
            subprocess.run(shinput, env=registery, shell=True)



main()

