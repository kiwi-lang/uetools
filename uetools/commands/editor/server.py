from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import add_arguments
from uetools.args.command import Command, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# fmt: off
@dataclass
class Arguments:
    map         : str           # Name of the map to serve
    project     : Optional[str] = None  # Name of the the project to open
    dedicated   : bool = False  # If true will start a dedicated server, otherwise a listen server (one local player that can host remote players)
    port        : int = 8123    # Server port
    dry         : bool = False  # Print the command it will execute without running it

@dataclass
class MapParameters:
    """Parameters added to the Map URL"""
    bIsLanMatch  : bool          = False
    bIsFromInvite: bool          = False
    spectatoronly: bool          = False
    gameinfo     : Optional[str] = None

# fmt: on


class Server(Command):
    """Launch the editor as a server

    Attributes
    ----------
    project: str
        Name of the project to serve

    map: str
        Name of the map to serve

    dedicated: bool
        If true starts a dedicated server, otherwise a listen server (one local player that can host remote players)

    Examples
    --------

    .. code-block:: console

       uecli server RTSGame

    """

    name: str = "server"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Server)
        add_arguments(parser, Arguments)
        add_arguments(parser, MapParameters)

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        cmd = [
            editor(),
            project,
        ]

        map_options = []

        if not args.dedicated:
            map_options.append("?listen")

        if args.bIsLanMatch:
            map_options.append("?bIsLanMatch=1")

        if args.bIsFromInvite:
            map_options.append("?bIsFromInvite=1")

        if args.spectatoronly:
            map_options.append("?spectatoronly")

        if args.gameinfo:
            map_options.append(f"?game={args.gameinfo}")

        mapname = args.map + "&".join(map_options)
        cmd.append(mapname)

        cmd.append(f"-port={args.port}")
        cmd.append("-game")

        if args.dedicated:
            cmd.append("-server")

        cmd.append("-FullStdOutLogOutput")
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Server
