import os

from uetools.args.command import Command, newparser
from uetools.core.conf import project_folder


class List(Command):
    """List projects"""

    name: str = "list"

    @staticmethod
    def arguments(subparsers):
        newparser(subparsers, List)

    @staticmethod
    def execute(args):
        folders = project_folder()

        for folder in folders:
            print(folder)
            for p in os.listdir(folder):
                if os.path.exists(os.path.join(folder, p, f"{p}.uproject")):
                    print("   -", p)


COMMANDS = List
