from dataclasses import asdict, dataclass

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# fmt: off
@dataclass
class Arguments:
    """Lauch a game setup for machine learning

    Attributes
    ----------
    project: str
        Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)

    Examples
    --------

    .. code-block:: console

       uecli ml RTSGame

       # Launch your agent script that will connect and make the agents play the game

    """
    resx                : int = 320
    resy                : int = 240
    fps                 : int = 20
    windowed            : bool = True
    usefixedtimestep    : bool = True
    game                : bool = True
    unattended          : bool = True
    onethread           : bool = False
    reducethreadusage   : bool = False
    nosound             : bool = False
    nullrhi             : bool = False
    deterministic       : bool = False
    debug               : bool = False
    mladapterport       : int = 8123    # RPC server listen port
# fmt: on


class ML(Command):
    """Lauch a game setup for machine learning"""

    name: str = "ml"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, ML)
        parser.add_argument("project", type=str, help="Name of the the project to open")
        parser.add_argument("map", type=str, help="Name of the map to open")
        parser.add_arguments(Arguments, dest="ml")
        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command it will execute without running it",
        )

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        # We found the project
        if project is not None:
            cmd = [editor(), project, args.map]

        # Assue the project is a path to the compiled project
        else:
            cmd = [args.project, args.map]

        cmd = cmd + command_builder(asdict(args.ml))

        print(" ".join(cmd))
        if not args.dry:
            fmt = Formatter()
            popen_with_format(fmt, cmd)


COMMANDS = ML
