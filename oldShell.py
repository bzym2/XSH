import os
import getpass
import socket
import sys

def logo(type="normal"):
    if type == "normal":
        print("\n       _       ____  _   _ \n"
              "    __| | __ _/ ___|| | | |\n"
              "   / _` |/ _` \___ \| |_| |\n"
              "  | (_| | (_| |___) |  _  |\n"
              "   \__,_|\__,_|____/|_| |_|\n")
    elif type == "text":
        print("i'll Define whAt means the ultimate SHell")

def set_prompt(style="default"):
    current_dir = os.getcwd()

    if style == "default":
        return f"┌──[{getpass.getuser()} on daSH]\n└──{current_dir}> "
    elif style == "classic":
        return f"[{getpass.getuser()}@{socket.gethostname()}] {current_dir}> "
    elif style == "power":
        return f"╓──[{getpass.getuser()} on daSH ~ {current_dir}]\n╙──{current_dir}> "
    elif style == "retro":
        return f"🐚 {current_dir} $ "
    elif style == "omega1":
        return f"┌──(Ø@{getpass.getuser()})\n└──{current_dir}> "
    elif style == "omega2":
        return f"┌──(ø@{getpass.getuser()})\n└──{current_dir}> "
    elif style == "kali":
        return f"┌──(kali㉿kali)-[~{current_dir}]\n└──$ "

def execute_command():

    prompt = set_prompt("classic")
    logo("normal")
    print("\nWelcome to daSH! Type 'exit' to quit.\n")

    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        elif user_input.lower().startswith("cd "):
            target_dir = user_input[3:].strip()
            try:
                if os.path.isdir(target_dir):
                    os.chdir(target_dir)
                else:
                    print(f"bash: cd: {target_dir}: No such file or directory")
            except Exception as e:
                print(f"Error: {e}")
        elif user_input:
            current_dir = os.getcwd()
            os.system(f"cd {current_dir} && {user_input}")

        else:
            print("Please enter a command.")

def main():
    execute_command()


if __name__ == "__main__":
    main()
    