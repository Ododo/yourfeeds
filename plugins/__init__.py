import pkgutil 
import importlib
from os import path

from yrfd import YRFD_PATH

__path__ = [path.join(YRFD_PATH, 'plugins')]

def get_plugins():
    for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix='plugins.'):
        yield importlib.import_module(modname)
