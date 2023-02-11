import uetools.commands.game
from uetools.core.command import ParentCommand


class Game(ParentCommand):
    """TBD"""

    name: str = "game"

    @staticmethod
    def module():
        return uetools.commands.game


COMMANDS = []
