import json
import os
import sys
import importlib.util

###################
pluginFolder = "./extensions"
###################

_Loaded = False
_allFoundFunctions = []
onLoadFunctions = {}
preHookFunctions = {}
afterHookFunctions = {}
getThemeFunctions = {}
loadPluginCount = 0
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
    oldPath = os.getcwd()
    global _Loaded, _allFoundFunctions, onLoadFunctions, preHookFunctions, afterHookFunctions, loadPluginCount
    os.chdir(pluginFolder)

    for file in os.listdir():
        if file.endswith('.py') and not file.startswith('_'):
            loadPluginCount += 1
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
                    _allFoundFunctions.append(f"{moduleName}.{funcName}")
                if funcName == 'onLoad':
                    onLoadFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'preHook':
                    preHookFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'afterHook':
                    afterHookFunctions[moduleName] = getattr(module, funcName)
                if funcName == 'getStyles':
                    getThemeFunctions[moduleName] = getattr(module, funcName)

    themeRefresh()
    os.chdir(oldPath)
    _Loaded = True

    if loadPluginCount != 0:
        print(f'[hushExtLoader] Loaded {loadPluginCount} plugins, {len(themes)} styles, {len(_allFoundFunctions)} functions.')
    
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