import importlib
import pkgutil

from uetools.core.cache import cache_to_local
from uetools.core.parallel import submit, as_completed


def discover_plugins_simple(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        plugins[name] = importlib.import_module(name)

    return plugins


def discover_plugins_parallel(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    futures = dict()
    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        f = submit(importlib.import_module, name)
        futures[f] = name
    
    for future in as_completed(futures):
        name = futures[future]
        module = future.result()
        plugins[name] = module

    return plugins


def discover_plugins(module):
    """Discover uetools plugins"""
    return  discover_plugins_parallel(module)


@cache_to_local("plugins")
def discover_plugins_command(module):
    modules = discover_plugins(module)
    all_commands = []

    for _, module in modules.items():
        if hasattr(module, "COMMANDS"):
            commands = getattr(module, "COMMANDS")

            if not isinstance(commands, list):
                commands = [commands]

            all_commands.extend(commands)
        
    return all_commands
