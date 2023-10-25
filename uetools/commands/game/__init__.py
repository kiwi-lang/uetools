from argklass.command import ParentCommand

import uetools.commands.game


class Game(ParentCommand):
    """TBD"""

    name: str = "game"

    @staticmethod
    def module():
        return uetools.commands.game


COMMANDS = []
