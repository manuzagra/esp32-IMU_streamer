def reload_module(mod):
    import sys
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)

def cat(file):
    with open(file) as f:
        print(f.read())

def is_file(path):
    try:
        with open(path) as f:
            pass
        return True
    except:
        return False
