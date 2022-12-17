from dataclasses import dataclass
from typing import Optional

from uetools.core.command import Command, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# This is not used technically, but we keep it for consistency with the other commands
# also help with the doc generation as this object appears on top
@dataclass
class Arguments:
    """Open the editor for a given project

    Attributes
    ----------
    project: str
        Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)

    address: str
        Address of the server to connect to, if None launch in standalone

    Examples
    --------

    .. code-block:: console

       uecli client RTSGameEditor

       uecli client RTSGameEditor --address localhost --port 8123

    """

    # name: str
    address: Optional[str] = None
    port: int = 8123  # Server port


class Client(Command):
    """Launch the editor as a client to an alredy running server"""

    name: str = "client"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Client)
        parser.add_argument("project", type=str, help="Name of the the project to open")
        parser.add_arguments(Arguments, dest="client")
        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command it will execute without running it",
        )

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        cmd = [editor(), project]

        if args.client.address:
            cmd.append(args.client.address)
            cmd.append(f"-port={args.client.port}")

        cmd.append("-game")
        cmd.append("-FullStdOutLogOutput")
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Client
