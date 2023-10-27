from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import editor, find_project
from uetools.core.options import projectfield
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


class Client(Command):
    """Launch the editor as a client, connecting to an already running server

    Attributes
    ----------
    project: str
        Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)

    address: str
        Address of the server to connect to, if None launch in standalone

    port: int
        Post of the server to connect to

    Examples
    --------

    .. code-block:: console

       uecli client RTSGameEditor

       uecli client RTSGameEditor --address localhost --port 8123

    """

    name: str = "client"

    @dataclass
    class Arguments:
        # fmt: off
        project: Optional[str] = projectfield()  # Name of the the project to open
        address: Optional[str] = '0.0.0.0'  # Address to the server
        port: int = 8123  # Server port
        dry: bool = False  # Print the command it will execute without running it
        # fmt: on

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        cmd = [editor(), project]

        if args.address:
            cmd.append(f"{args.address}:{args.port}")

        cmd.append("-game")
        cmd.append("-FullStdOutLogOutput")
        cmd.append("-Log")
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Client
