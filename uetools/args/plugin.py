import importlib
import pkgutil
import glob
import os
import traceback

from uetools.core.perf import timeit
from uetools.args.parallel import submit, as_completed
from uetools.args.cache import cache_to_local


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
    return discover_plugins_parallel(module)


def _discover_plugin_commands(module):
    with timeit("discover_plugin_commands"):
        modules = discover_plugins(module)
        all_commands = []

        for _, module in modules.items():
            if hasattr(module, "COMMANDS"):
                commands = getattr(module, "COMMANDS")

                if not isinstance(commands, list):
                    commands = [commands]

                all_commands.extend(commands)

        return all_commands


def discover_plugin_commands(module):
    cached_call = cache_to_local(module.__name__)(_discover_plugin_commands)
    return cached_call(module)


def _resolve_factory_module(base_file_name, base_module, function_name, module_path):
    module_file = module_path.split(os.sep)[-1]

    if module_file == base_file_name:
        return

    module_name = module_file.split(".py")[0]

    try:
        path = ".".join([base_module, module_name])

        module = __import__(path, fromlist=[""])

        if hasattr(module, function_name):
            return getattr(module, function_name)

    except ImportError:
        print(traceback.format_exc())
        return


def fetch_factories_parallel(
    registry, base_module, base_file_name, function_name="COMMANDS"
):
    """Loads all the defined commands"""

    module_path = os.path.dirname(os.path.abspath(base_file_name))
    paths = list(glob.glob(os.path.join(module_path, "[A-Za-z]*"), recursive=False))

    futures = []
    for path in paths:
        args = (base_file_name, base_module, function_name, path)
        futures.append(submit(_resolve_factory_module, *args))

    for future in as_completed(futures):
        cmd = future.result()

        if cmd is not None:
            registry.insert_commands(cmd)


def fetch_factories_single(
    registry, base_module, base_file_name, function_name="COMMANDS"
):
    """Loads all the defined commands"""
    module_path = os.path.dirname(os.path.abspath(base_file_name))

    for module_path in glob.glob(
        os.path.join(module_path, "[A-Za-z]*"), recursive=False
    ):

        cmd = _resolve_factory_module(
            base_file_name, base_module, function_name, module_path
        )
        if cmd is not None:
            registry.insert_commands(cmd)


def fetch_factories(registry, base_module, base_file_name, function_name="COMMANDS"):
    fetch_factories_parallel(registry, base_module, base_file_name, function_name)


def discover_from_plugins_commands(registry, module, function_name="COMMANDS"):
    """Imports all commands for the plugins we found"""
    plugins = discover_plugins(module)

    for _, plugin in plugins.items():
        if hasattr(plugin, function_name):
            plugin_commands = getattr(plugin, function_name)
            registry.insert_commands(plugin_commands)


# pylint: disable=too-few-public-methods
class CommandRegistry:
    """Simple class to keep track of all the commands we find"""

    def __init__(self):
        self.found_commands = {}

    def insert_commands(self, cmds):
        """Insert a command into the registry makes sure it is unique"""
        if not isinstance(cmds, list):
            cmds = [cmds]

        for cmd in cmds:
            if cmd.name != cmd.name.strip():
                print(f"Warning: {cmd.name} has white space before or after the name")

            assert (
                cmd.name not in self.found_commands
            ), f"Duplicate command name: {cmd.name}"
            self.found_commands[cmd.name] = cmd

    def fix_nondeterminism(self):
        data = self.__getstate__()
        self.__setstate__(data)

    def __getstate__(self):
        return sorted(self.found_commands.items(), key=lambda x: x[0])

    def __setstate__(self, d):
        self.found_commands = {k: v for k, v in d}


@cache_to_local("commands")
def discover_module_commands(module, plugin_module=None):
    """Discover all the commands we can find (plugins and built-in)"""
    registry = CommandRegistry()

    with timeit("fetch_factories"):
        fetch_factories(registry, module.__name__, module.__file__)

    if plugin_module is not None:
        with timeit("discover_plugins"):
            discover_from_plugins_commands(registry, plugin_module)

    registry.fix_nondeterminism()
    return registry
