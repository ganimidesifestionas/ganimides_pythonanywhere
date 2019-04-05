import importlib

def import_module(global_vars, root, modules):
    for m in modules
        try:
            global_vars[m] = importlib.import_module(root + '.' + m)
        except ImportError:
            global_vars[m] = importlib.import_module(m)
            