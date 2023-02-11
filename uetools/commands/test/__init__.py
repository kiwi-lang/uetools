import uetools.commands.test
from uetools.core.command import ParentCommand


class Test(ParentCommand):
    """Set of commands to run automated tests"""

    name: str = "test"

    @staticmethod
    def module():
        return uetools.commands.test


COMMANDS = Test
