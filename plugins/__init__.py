import pkgutil 
import importlib
from os import path

from yrfd import PLUGINS_PATH

__path__ = [PLUGINS_PATH]

def get_plugins():
    for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix='plugins.'):
        yield importlib.import_module(modname)
