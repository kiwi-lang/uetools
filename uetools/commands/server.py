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

    # project: str
    # map: str
    dedicated: bool = False  # If true will start a dedicated server, otherwise a listen server (one local player that can host remote players)
    port: int = 8123  # Server port


@dataclass
class MapParameters:
    """Parameters added to the Map URL"""

    bIsLanMatch: bool = False
    bIsFromInvite: bool = False
    spectatoronly: bool = False
    gameinfo: Optional[str] = None


class Server(Command):
    """Launch the editor as a server"""

    name: str = "server"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Server)

        # this makes it ugly
        # editor.add_arguments(Arguments, dest="server")

        parser.add_argument(
            "project", metavar="project", type=str, help="Name of the project to serve"
        )
        parser.add_argument(
            "map",
            metavar="map",
            type=str,
            help=" Name of the map to serve (if the map is located inside the map folder, just the name of the map is needed,"
            "if not the full path is needed including the extension, e.g. /Game/NotMap/MyMap.umap)",
        )
        parser.add_arguments(Arguments, dest="args")
        parser.add_arguments(MapParameters, dest="params")
        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command it will execute without running it",
        )

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
