# author: bzym2
# describe: Example plugin.
import os
import shutil



def registerCommands():
    return {
        'ls': ls_command,
        'cp': cp_command,
        'mv': mv_command,
        'rm': rm_command,
        'touch': touch_command
    }

def ls_command(args):
    """Lists the contents of a directory."""
    if len(args) > 1:
        path = args[1]
    else:
        path = os.getcwd()
    
    try:
        files = os.listdir(path)
        print("\n".join(files))
    except FileNotFoundError:
        print(f"Error: Directory {path} not found.")

def cp_command(args):
    """Copies a file."""
    if len(args) == 3:
        src, dst = args[1], args[2]
        try:
            shutil.copy(src, dst)
            print(f"Copied {src} to {dst}.")
        except FileNotFoundError:
            print(f"Error: {src} not found.")
    else:
        print("Usage: cp <source> <destination>")

def mv_command(args):
    """Moves a file."""
    if len(args) == 3:
        src, dst = args[1], args[2]
        try:
            shutil.move(src, dst)
            print(f"Moved {src} to {dst}.")
        except FileNotFoundError:
            print(f"Error: {src} not found.")
    else:
        print("Usage: mv <source> <destination>")

def rm_command(args):
    """Removes a file."""
    if len(args) == 2:
        file = args[1]
        try:
            os.remove(file)
            print(f"Removed {file}.")
        except FileNotFoundError:
            print(f"Error: {file} not found.")
    else:
        print("Usage: rm <file>")

def touch_command(args):
    """Creates an empty file or updates the timestamp."""
    if len(args) == 2:
        file = args[1]
        with open(file, 'a'):
            os.utime(file, None)  # Update the timestamp
        print(f"Touched {file}.")
    else:
        print("Usage: touch <file>")

def getStyles():
    return {
        'fileops_theme': 'fileops> $ '  # Custom theme for file operations
    }