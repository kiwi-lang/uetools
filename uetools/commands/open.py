from dataclasses import dataclass

from uetools.core.command import Command, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import run


# This is not used technically, but we keep it for consistency with the other commands
# also help with the doc generation as this object appears on top
@dataclass
class Arguments:
    """Open the editor for a given project

    Attributes
    ----------
    name: str
        Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)

    Examples
    --------

    .. code-block:: console

       uecli open RTSGameEditor

    """

    name: str  # Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)


class Open(Command):
    """Open the editor for a given project"""

    name: str = "open"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Open)
        # this makes it ugly
        # editor.add_arguments(Arguments, dest="open")

        parser.add_argument("name", type=str, help="Name of the the project to open")

    @staticmethod
    def execute(args):
        project = find_project(args.name)

        return run([editor(), project], check=True).returncode


COMMANDS = Open
