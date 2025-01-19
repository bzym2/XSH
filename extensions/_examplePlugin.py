# Enable this plugin by removing the '_' at the start of the filename.

def onLoad():
    _thisFunctionWillNotBeExecutedByExtensionLoader()

def preHook():
    pass

def afterHook():
    pass

def getStyles():
    return {
        'testStyle_1': '> ',
        'testStyle_2': '>> ', 
    }

def _thisFunctionWillNotBeExecutedByExtensionLoader():
    print("Hello, World!")