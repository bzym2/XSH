import os
import time
def write(message: str):
    with open(f"./logs/.logs", 'a+') as f:
        f.write(f'({time.time()})[ExtensionLoader] {message}\n')
def onLoad():
    write("System initializing")
    if not os.path.exists("./extensions"):
        os.mkdir("./extensions")
        write("Ext dir not found.Created extensions directory.")
    write(os.listdir("./extensions"))
    for i in os.listdir("./extensions"):
        if i.endswith(".py"):
            exec(open(f"./extensions/{i}").read())
            write(f"Loaded {i}")
if __name__ == "__main__":
    onLoad()