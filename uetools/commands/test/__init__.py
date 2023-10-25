from argklass.command import ParentCommand

import uetools.commands.test


class Test(ParentCommand):
    """Set of commands to run automated tests"""

    name: str = "test"

    @staticmethod
    def module():
        return uetools.commands.test


COMMANDS = Test
