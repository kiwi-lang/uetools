from dataclasses import asdict, dataclass

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# fmt: off
@dataclass
class Arguments:
    """Launch a game setup for machine learning

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
    resx                : int = 320     # resolution width
    resy                : int = 240     # resolution height
    fps                 : int = 20      # Max FPS
    windowed            : bool = True   # Window mode
    usefixedtimestep    : bool = True   # Block until the ML agent replies with an action
    game                : bool = True   #
    unattended          : bool = True   # Close when the game finishes
    onethread           : bool = False  # Run on a single thread
    reducethreadusage   : bool = False  #
    nosound             : bool = False  # Disable sound
    nullrhi             : bool = False  # Disable rendering
    deterministic       : bool = False  # Set seeds ?
    debug               : bool = False  #
    mladapterport       : int = 8123    # RPC server listen port
# fmt: on


class ML(Command):
    """Launch a game setup for machine learning"""

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

        # Assume the project is a path to the compiled project
        else:
            cmd = [args.project, args.map]

        cmd = cmd + command_builder(asdict(args.ml))

        print(" ".join(cmd))
        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = ML
