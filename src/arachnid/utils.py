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


def resolve_middleware(module_name):
    pass


def load_module(path):
    path = os.path.abspath(path)
    path, _ = path.rsplit('.', 1)
    directory, module = path.rsplit('/', 1)
    sys.path.insert(0, directory)
    mod = importlib.import_module(module)
    sys.path.remove(directory)
    return mod, directory


def load_module_obj(path):
    mod, directory = load_module(path)
    obj_name = path.rsplit('.')[1]
    return getattr(mod, obj_name)


def load_settings(path):
    mod, directory = load_module(path)

    for spider in mod.spiders:
        if not '/' in spider['spider']:
            spider['spider'] = os.path.join(directory, spider['spider'])

        for mw_type in ['spider_middleware', 'downloader_middleware', 'result_middleware']:
            for idx, mw in enumerate(spider.get(mw_type, [])):
                mw = os.path.join(directory, mw)
                spider[mw_type][idx] = mw
    return mod

