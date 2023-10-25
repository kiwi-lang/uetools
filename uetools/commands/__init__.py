from argklass.cache import get_cache_future, get_cache_status
from argklass.plugin import discover_module_commands


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
