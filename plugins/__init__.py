import pkgutil 
import importlib
from os import path


def get_plugins(PLUGINS_PATH):
    global __path__
    __path__ = [PLUGINS_PATH]
    for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix='plugins.'):
        yield importlib.import_module(modname)
