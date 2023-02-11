import logging
import sys
from dataclasses import dataclass

from uetools.core.arguments import add_arguments
from uetools.core.command import Command, newparser
from uetools.format.base import Formatter
from uetools.format.cooking import CookingFormatter
from uetools.format.tests import TestFormatter

log = logging.getLogger()


profiles = {
    None: Formatter,
    "cooking": CookingFormatter,
    "tests": TestFormatter,
}


@dataclass
class Arguments:
    """Format UnrealEngine log output. It will attempt to align log output to make them more readable.

    Attributes
    ----------
    profile: str
        Formatting profile to use (None, cooking, tests)

    file: str
        File to format, if none it will use stdin

    fail_on_error:
        the program will exit with an error code if errors were found

    col: int
        The size of the category column

    Examples
    --------

    .. code-block:: console

       uecli fmt --profile cooking --file RTSGame.log

       ../UnrealEditor ... | uecli fmt
       [  0][L][LogWindows           ] Failed to load 'aqProf.dll' (GetLastError=126)
       [  0][L][LogWindows           ] File 'aqProf.dll' does not exist
       [  0][L][LogProfilingDebugging] Loading WinPixEventRuntime.dll for PIX profiling (from ../../../Engine/Binaries/ThirdParty/Windows/WinPixEventRuntime/x64).
       [  0][D][LogConfig            ]  Loading HoloLens ini files took 0.02 seconds
       [  0][D][LogConfig            ]  Loading Android ini files took 0.02 seconds
       [  0][D][LogConfig            ]  Loading Unix ini files took 0.03 seconds
       [  0][D][LogConfig            ]  Loading Windows ini files took 0.03 seconds
       [  0][D][LogConfig            ]  Loading TVOS ini files took 0.03 seconds
       [  0][D][LogConfig            ]  Loading Linux ini files took 0.03 seconds
       [  0][D][LogConfig            ]  Loading LinuxArm64 ini files took 0.03 seconds
       [  0][L][LogPluginManager     ] Mounting Engine plugin FastBuildController

    """

    profile: str = None
    file: str = None
    fail_on_error: bool = False
    col: int = 24


class Format(Command):
    """Format UnrealEngine log output. It will attempt to align log output to make them more easily readable."""

    name: str = "format"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Format)
        add_arguments(parser, Arguments)

    def __init__(self, profile=None):
        self.profile = profile

    @staticmethod
    def execute(args):
        args = args.args
        fmt = profiles.get(args.profile, Formatter)(args.col)

        if args.file is not None:
            with open(args.file, encoding="utf-8") as file:
                for line in file:
                    fmt.match_regex(line)

            if args.fail_on_error and len(fmt.bad_logs) > 0:
                return 1
            return 0

        for line in sys.stdin:
            fmt.match_regex(line)

        print("-" * 80)
        print("    Summary")
        print("=" * 80)
        for line in fmt.bad_logs:
            print("  - ", end="")
            Formatter.format(fmt, **line)
        print("=" * 80)

        if args.fail_on_error and len(fmt.bad_logs) > 0:
            return 1

        return 0


logging.basicConfig(level=logging.CRITICAL)

COMMANDS = Format
