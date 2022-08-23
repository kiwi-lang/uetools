from dataclasses import dataclass
import os
import subprocess

from uetools.conf import (
    Command,
    editor,
    load_conf
)


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
    name: str


class Open(Command):
    """Open the editor for a given project"""

    name: str = "open"

    @staticmethod
    def arguments(subparsers):
        editor = subparsers.add_parser(Open.name, help="Open an Unreal Engine porject")
        # this makes it ugly
        # editor.add_arguments(Arguments, dest="open")

        editor.add_argument('name', type=str, help='Name of the the project to open')

    @staticmethod
    def execute(args):

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, args.name)
        uproject = os.path.join(project_folder, f"{args.name}.uproject")

        subprocess.run([editor(), uproject])


COMMAND = Open
