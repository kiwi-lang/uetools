from argklass.command import ParentCommand

import uetools.commands.uat


class UAT(ParentCommand):
    """Unreal Automation Tool Commands"""

    name: str = "uat"

    @staticmethod
    def module():
        return uetools.commands.uat


COMMANDS = UAT
