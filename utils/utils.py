def reload_module(mod):
    import sys
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)

def cat(file):
    with open(file) as f:
        print(f.read())

def exist(path):
    import os
    try:
        os.stat(path)
        return True
    except:
        return False

def is_file(path):
    import os
    try:
        return bool(os.stat(path)[6])
    except:
        return False

def is_dir(path):
    import os
    try:
        return not bool(os.stat(path)[6])
    except:
        return False
