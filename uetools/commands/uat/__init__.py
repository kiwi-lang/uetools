import uetools.commands.uat
from uetools.core.command import ParentCommand


class UAT(ParentCommand):
    """Unreal Automation Tool Commands"""

    name: str = "uat"

    @staticmethod
    def module():
        return uetools.commands.uat


COMMANDS = UAT
