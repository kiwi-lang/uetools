from argklass.cache import get_cache_future, get_cache_status, cache_to_local
from argklass.plugin import discover_module_commands_no_cache



@cache_to_local("commands", location=__name__)
def discover_module_commands(module, plugin_module=None):
    """Discover all the commands we can find (plugins and built-in)"""
    return discover_module_commands_no_cache(module, plugin_module)



def discover_commands():
    import uetools.commands
    import uetools.plugins

    return discover_module_commands(uetools.commands, uetools.plugins).found_commands


def find_command(name):
    return discover_commands().get(name)


def command_cache_status():
    return get_cache_status("commands")


def command_cache_future():
    return get_cache_future("commands")
