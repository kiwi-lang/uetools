from uetools.args.command import Command, newparser


class ProjectNew(Command):
    """WIP Create a new project"""

    name: str = "new"

    @staticmethod
    def arguments(subparsers):
        newparser(subparsers, ProjectNew)

    @staticmethod
    def execute(args):
        print("here")


# COMMANDS = ProjectNew
