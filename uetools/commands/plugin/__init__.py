from argklass.command import ParentCommand

import uetools.commands.plugin


class Plugin(ParentCommand):
    """Set of commands to create, package and publish plugins"""

    name: str = "plugin"

    @staticmethod
    def module():
        return uetools.commands.plugin


COMMANDS = Plugin
