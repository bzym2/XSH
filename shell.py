import os
import getpass
import platform

theme = "bash"

print("Welcome to Hush. A sleek, ultra-lightweight, and extensible shell.")

def getPrefix(theme: str = ''):
    style = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# "
    }
    return style.get(theme, '$ ')

def main():
    while True:
        shinput = input(getPrefix(theme))


        if not shinput:
            pass
        
        elif shinput == 'quit' or shinput == 'exit':
            exit()

        elif shinput.startswith('cd '):
            try:
                os.chdir(shinput.split(' ')[-1])
            except:
                print(f'hush: cd: can\'t cd to {shinput.split(" ")[-1]}')
        
        else:
            os.system(shinput)


try:
    main()
except:
    exit()