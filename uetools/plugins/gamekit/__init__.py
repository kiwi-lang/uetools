from uetools.args.command import ParentCommand


class Gamekit(ParentCommand):
    """Set of commands for Gamekit"""

    name: str = "gamekit"

    @staticmethod
    def module():
        import uetools.plugins.gamekit

        return uetools.plugins.gamekit


COMMANDS = Gamekit
