import os
import importlib.util

###################
pluginFolder = "./extensions"
###################

_Loaded = False
_allFoundFunctions = []
onLoadFunctions = []
preHookFunctions = []
afterHookFunctions = []
loadPluginCount = 0


def pluginLoad():
    global _Loaded, _allFoundFunctions, onLoadFunctions, preHookFunctions, afterHookFunctions, loadPluginCount
    os.chdir(pluginFolder)

    for file in os.listdir():
        if file.endswith('.py') and not file.startswith('_'):
            loadPluginCount += 1
            spec = importlib.util.spec_from_file_location(file[:-3], file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for func_name in dir(module):
                if callable(getattr(module, func_name)) and not func_name.startswith("__"):
                    _allFoundFunctions.append(func_name)
                if func_name == 'onLoad':
                    onLoadFunctions.append(getattr(module, func_name))
                if func_name == 'preHook':
                    preHookFunctions.append(getattr(module, func_name))
                if func_name == 'afterHook':
                    afterHookFunctions.append(getattr(module, func_name))
    _Loaded = True
