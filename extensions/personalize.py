logo_default = """
  _   _           _     
 | | | |_   _ ___| |__  
 | |_| | | | / __| '_ \ 
 |  _  | |_| \__ \ | | |
 |_| |_|\__,_|___/_| |_|
                        
"""
logo_big = """
  _    _           _     
 | |  | |         | |    
 | |__| |_   _ ___| |__  
 |  __  | | | / __| '_ \ 
 | |  | | |_| \__ \ | | |
 |_|  |_|\__,_|___/_| |_|
                         
"""
logo_roman = """

ooooo   ooooo                      oooo        
`888'   `888'                      `888        
 888     888  oooo  oooo   .oooo.o  888 .oo.   
 888ooooo888  `888  `888  d88(  "8  888P"Y88b  
 888     888   888   888  `"Y88b.   888   888  
 888     888   888   888  o.  )88b  888   888  
o888o   o888o  `V88V"V8P' 8""888P' o888o o888o 
                                               
"""
logo_ansi_shadow = """

██╗  ██╗██╗   ██╗███████╗██╗  ██╗
██║  ██║██║   ██║██╔════╝██║  ██║
███████║██║   ██║███████╗███████║
██╔══██║██║   ██║╚════██║██╔══██║
██║  ██║╚██████╔╝███████║██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                 
"""
logo_colossal = """

888    888                   888      
888    888                   888      
888    888                   888      
8888888888 888  888 .d8888b  88888b.  
888    888 888  888 88K      888 "88b 
888    888 888  888 "Y8888b. 888  888 
888    888 Y88b 888      X88 888  888 
888    888  "Y88888  88888P' 888  888 
                                      
"""
logo_slant = """

    __  __           __  
   / / / __  _______/ /_ 
  / /_/ / / / / ___/ __ \\
 / __  / /_/ (__  / / / /
/_/ /_/\__,_/____/_/ /_/ 
                         
"""

import getpass
import os
import platform
from colorama import Fore, Style, init

def getStyles():
    theme = {
        'bash': f"{getpass.getuser()}@{platform.node()}:{os.getcwd().replace(os.path.expanduser('~'), '~')}# ",
        'colored_bash': f"{Style.BRIGHT}{Fore.GREEN}{getpass.getuser()}@{platform.node()}{Fore.BLUE}:{os.getcwd().replace(os.path.expanduser('~'), '~')}{Style.RESET_ALL}$ ",
        'fish': f"{Fore.LIGHTGREEN_EX}{getpass.getuser()}{Style.RESET_ALL}@{platform.node()} {Fore.RED}{os.getcwd().replace(os.path.expanduser('~'), '~')}{Style.RESET_ALL}# ",
        'kali': f"{Fore.BLUE}┌──({getpass.getuser()}㉿{Fore.RED}kali{Fore.BLUE})-[{os.getcwd().replace(os.path.expanduser('~'), '~')}]\n└──{Fore.RESET}$ ",
        'hush': f"╭─[{getpass.getuser()} on Hush]\n╰─{os.getcwd().replace(os.path.expanduser('~'), '~')}> ",
        'omega': f"╭──(ø@{getpass.getuser()})\n╰──{os.getcwd().replace(os.path.expanduser('~'), '~')}> "
    }
    return theme


logo = logo_default
motd = "Welcome to Hush."
theme = 'colored_bash'

def onLoad():
    print(logo)
    print(motd)

def preHook():
    pass

def afterHook():
    pass


