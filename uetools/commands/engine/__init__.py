import uetools.commands.engine
from uetools.core.command import ParentCommand


class Engine(ParentCommand):
    """Set of commands to manage engine installation/source"""

    name: str = "engine"

    @staticmethod
    def module():
        return uetools.commands.engine


COMMANDS = Engine
