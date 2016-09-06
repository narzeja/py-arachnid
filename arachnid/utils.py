from .spider import Spider

import importlib
import inspect
import os.path
import sys


def load_spider(module, path=None):
    if path:
        sys.path.insert(0, path)
    members = inspect.getmembers(module)
    for name, mod in members:
        if issubclass(mod, Spider):
            if path:
                sys.path.remove(path)
            return mod


def load_module(path):
    path = os.path.abspath(path)
    path, _ = path.rsplit('.', 1)
    directory, module = path.rsplit('/', 1)
    sys.path.insert(0, directory)
    mod = importlib.import_module(module)
    sys.path.remove(directory)
    return mod


def load_settings(path):
    path = os.path.abspath(path)
    path, _ = path.rsplit('.', 1)
    directory, module = path.rsplit('/', 1)
    sys.path.insert(0, directory)
    mod = importlib.import_module(module)
    for spider in mod.spiders:
        if not '/' in spider['spider']:
            spider['spider'] = os.path.join(directory, spider['spider'])
    sys.path.remove(directory)
    return mod
