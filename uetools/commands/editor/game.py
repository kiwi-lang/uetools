from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import editor, find_project
from uetools.core.options import projectfield
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


class Game(Command):
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

       uecli game RTSGameEditor

       uecli game RTSGameEditor

    """

    name: str = "game"

    @dataclass
    class Arguments:
        # fmt: off
        project: Optional[str] = projectfield()  # Name of the the project to open
        dry: bool = False  # Print the command it will execute without running it
        # fmt: on

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        cmd = [editor(), project]

        cmd.append("-game")
        cmd.append("-FullStdOutLogOutput")
        cmd.append("-Log")
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Game
