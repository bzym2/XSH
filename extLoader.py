import os
import importlib.util

###################
plugin_folder = "./extensions"
###################

_loadCount = 0

def pluginsLoad():
    global _loadCount
    os.chdir(plugin_folder)
    functions = []

    for file in os.listdir():
        if file.endswith('.py'):
            spec = importlib.util.spec_from_file_location(file[:-3], file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "onLoad"): 
                functions.append(module.onLoad)
                _loadCount += 1
            else: 
                print(f"[extLoader] Can't load plugin: {file[:-3]}")


    return functions