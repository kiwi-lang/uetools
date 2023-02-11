import uetools.plugins.gamekit
from uetools.core.command import ParentCommand


class Gamekit(ParentCommand):
    """Set of commands for Gamekit"""

    name: str = "gamekit"

    @staticmethod
    def module():
        return uetools.plugins.gamekit


COMMANDS = Gamekit
