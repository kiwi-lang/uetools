from uetools.args.plugin import discover_module_commands
from uetools.args.cache import get_cache_status, get_cache_future


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
