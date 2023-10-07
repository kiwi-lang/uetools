import glob
import os
import traceback

from uetools.core.perf import timeit
from uetools.core.plugin import discover_plugins
from uetools.core.parallel import submit, as_completed
from uetools.core.cache import cache_to_local, get_cache_status

try:
    import uetools.plugins

    PLUGINS = True

except ModuleNotFoundError:
    PLUGINS = False

except ImportError:
    PLUGINS = False


def _resolve_factory_module(base_file_name, base_module, function_name, module_path):
    module_file = module_path.split(os.sep)[-1]

    if module_file == base_file_name:
        return

    module_name = module_file.split(".py")[0]

    try:
        module = __import__(".".join([base_module, module_name]), fromlist=[""])

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


def command_cache_status():
    return get_cache_status("commands")


@cache_to_local("commands")
def _discover_commands():
    """Discover all the commands we can find (plugins and built-in)"""
    registry = CommandRegistry()

    with timeit("fetch_factories"):
        fetch_factories(registry, "uetools.commands", __file__)

    if PLUGINS:
        with timeit("discover_plugins"):
            discover_from_plugins_commands(registry, uetools.plugins)

    registry.fix_nondeterminism()
    return registry


def discover_commands():
    return _discover_commands().found_commands


def find_command(name):
    return discover_commands().get(name)
