from dataclasses import dataclass
from typing import Optional

from uetools.core.arguments import add_arguments
from uetools.core.command import Command, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# fmt: off
@dataclass
class Arguments:
    project     : str           #: Name of the project to serve
    map         : str           #: Name of the map to serve
    dedicated   : bool = False  #: If true will start a dedicated server, otherwise a listen server (one local player that can host remote players)
    port        : int = 8123    #: Server port
    dry         : bool = False  #: Print the command it will execute without running it

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

        if not args.args.dedicated:
            map_options.append("?listen")

        if args.params.bIsLanMatch:
            map_options.append("?bIsLanMatch=1")

        if args.params.bIsFromInvite:
            map_options.append("?bIsFromInvite=1")

        if args.params.spectatoronly:
            map_options.append("?spectatoronly")

        if args.params.gameinfo:
            map_options.append(f"?game={args.params.gameinfo}")

        mapname = args.map + "&".join(map_options)
        cmd.append(mapname)

        cmd.append(f"-port={args.args.port}")
        cmd.append("-game")

        if args.args.dedicated:
            cmd.append("-server")

        cmd.append("-FullStdOutLogOutput")
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Server
