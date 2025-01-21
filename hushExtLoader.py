import json
import os
import sys
import importlib.util

###################
pluginFolder = "./extensions"
###################

Loaded = False
allFoundFunctions = []
onLoadFunctions = {}
preHookFunctions = {}
afterHookFunctions = {}
registerCommandFunctions = {}
registeredCommands = {}
getThemeFunctions = {}
loadedPlugins = []
themes = {}
Logs = []

def _isSerializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

def Dump():
    _globalsFiltered = {}
            
    for key, value in globals().items():
        if _isSerializable(value):
            _globalsFiltered[key] = value
    return _globalsFiltered

def print(string):
    Logs.append(string)
    sys.stdout.write(f'{string}\n')

def Load():
    global Loaded, allFoundFunctions, onLoadFunctions, preHookFunctions, afterHookFunctions, loadedPlugins

    oldPath = os.getcwd()
    os.chdir(pluginFolder)

    for file in os.listdir():
        if file.endswith('.py') and not file.startswith('_'):
            moduleName = file[:-3]
            spec = importlib.util.spec_from_file_location(moduleName, file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as f:
                print(f'[hushExtLoader] Failed load plugin \"{moduleName}\": {f}.')
                continue
            for funcName in dir(module):
                if callable(getattr(module, funcName)) and not funcName.startswith("__"):
                    allFoundFunctions.append(f"{moduleName}.{funcName}")
                if funcName == 'onLoad':
                    onLoadFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'preHook':
                    preHookFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'afterHook':
                    afterHookFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'getStyles':
                    getThemeFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'registerCommands':
                    registerCommandFunctions[moduleName] = getattr(module, funcName)

            loadedPlugins.append(moduleName)

    themeRefresh()
    commandBind()
    os.chdir(oldPath)
    Loaded = True

    if len(loadedPlugins) != 0:
        print(f'[hushExtLoader] Loaded {len(loadedPlugins)} plugins, {len(themes)} styles, {len(allFoundFunctions)} functions, {len(registeredCommands)} custom commands.')
    
def runPluginInit():
    try:
        for function in onLoadFunctions: onLoadFunctions[function]()
    except Exception as f:
        print(f'[hushExtLoader] Error in running plugin {function}\'s init: {f}')

def runPluginPreHook():
    try:
        for function in preHookFunctions: preHookFunctions[function]()
    except Exception as f:
        print(f'[hushExtLoader] Error in running plugin {function}\'s pre-hook function: {f}')

def runPluginAfterHook():
    try:
        for function in afterHookFunctions: afterHookFunctions[function]()
    except Exception as f:
        print(f'[hushExtLoader] Error in running plugin {function}\'s after-hook function: {f}')

def themeRefresh():
    global themes, getThemeFunctions

    themes = {}
    for moduleName in getThemeFunctions:
        moduleTheme = getThemeFunctions[moduleName]()
        for theme in moduleTheme:
            themes[f'{moduleName}.{theme}'] = moduleTheme[theme]

def commandBind():
    global registeredCommands, registerCommandFunctions

    registeredCommands = {}
    for moduleName in registerCommandFunctions:
        moduleCommand = registerCommandFunctions[moduleName]()
        for command in moduleCommand:
            if command[0] == '#':
                registeredCommands[f'{command[1:]}'] = moduleCommand[command]
                registeredCommands[f'{moduleName}.{command}'] = moduleCommand[command]
            else:
                registeredCommands[f'{moduleName}.{command}'] = moduleCommand[command]