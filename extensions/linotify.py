import getpass
import os
import platform
from colorama import Fore, Style, Back

noticeIcon = f'{Back}'

def preHook():
    pass

def getStyles():
    return {
        'colored_bash': f"{Style.BRIGHT}{Fore.GREEN}{getpass.getuser()}@{platform.node()}{Fore.BLUE}:{os.getcwd().replace(os.path.expanduser('~'), '~')}{Style.RESET_ALL}$ ",
    }
