from argklass.command import ParentCommand

import uetools.commands.ubt


class UBT(ParentCommand):
    """Unreal Build Tool Commands"""

    name: str = "ubt"

    @staticmethod
    def module():
        return uetools.commands.ubt


COMMANDS = UBT
