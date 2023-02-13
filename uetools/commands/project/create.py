from uetools.core.command import Command, newparser


class ProjectNew(Command):
    """WIP Create a new project"""

    name: str = "new"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, ProjectNew)

    @staticmethod
    def execute(args):
        print("here")


#: COMMANDS = ProjectNew
