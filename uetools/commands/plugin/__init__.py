import uetools.commands.plugin
from uetools.args.command import ParentCommand


class Plugin(ParentCommand):
    """Set of commands to create, package and publish plugins"""

    name: str = "plugin"

    @staticmethod
    def module():
        return uetools.commands.plugin


COMMANDS = Plugin
