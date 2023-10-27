from argklass.command import ParentCommand


class Game(ParentCommand):
    """TBD"""

    name: str = "game"

    @staticmethod
    def module():
        import uetools.commands.game

        return uetools.commands.game


COMMANDS = Game
