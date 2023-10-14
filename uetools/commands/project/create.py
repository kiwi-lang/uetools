from dataclasses import dataclass

from uetools.args.command import Command


class ProjectNew(Command):
    """WIP Create a new project"""

    name: str = "new"

    @dataclass
    class Arguments:
        pass

    @staticmethod
    def execute(args):
        print("here")


# COMMANDS = ProjectNew
