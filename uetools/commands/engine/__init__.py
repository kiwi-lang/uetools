from argklass.command import ParentCommand

import uetools.commands.engine


class Engine(ParentCommand):
    """Set of commands to manage engine installation/source"""

    name: str = "engine"

    @staticmethod
    def module():
        return uetools.commands.engine


COMMANDS = Engine
