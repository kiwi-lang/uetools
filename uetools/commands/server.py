import os
import subprocess
from dataclasses import dataclass

from uetools.command import Command
from uetools.conf import editor, load_conf


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


class Server(Command):
    """Launch the editor as a client to an alredy running server"""

    name: str = "server"

    @staticmethod
    def arguments(subparsers):
        editor_args = subparsers.add_parser(
            Server.name,
            help="Launch the editor as a client to an alredy running server",
        )
        # this makes it ugly
        # editor.add_arguments(Arguments, dest="open")

        editor_args.add_argument("name", type=str, help="Name of the the project to open")

    @staticmethod
    def execute(args):

        # listen
        # bIsLanMatch
        # bIsFromInvite
        # spectatoronly

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, args.name)
        uproject = os.path.join(project_folder, f"{args.name}.uproject")

        subprocess.run(
            [
                editor(),
                uproject,
                map + "?listen",
                "-server",
            ],
            check=True,
        )


COMMAND = Server
