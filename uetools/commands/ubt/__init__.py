import uetools.commands.ubt
from uetools.core.command import ParentCommand


class UBT(ParentCommand):
    """Unreal Build Tool Commands"""

    name: str = "ubt"

    @staticmethod
    def module():
        return uetools.commands.ubt


COMMANDS = UBT
