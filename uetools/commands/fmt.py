import logging
import sys
from dataclasses import dataclass

from uetools.command import Command
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
    """Format UnrealEngine log output. It will attempt to align log output to make them more easily readable.

    Attributes
    ----------
    profile: str
        Formating profile to use (None, cooking, tests)

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

       UnrealEditor | uecli fmt

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
        fmt = subparsers.add_parser(Format.name, help="Format UnrealEngine logs")
        fmt.add_arguments(Arguments, dest="args")

    def __init__(self, profile=None):
        self.profile = profile

    @staticmethod
    def execute(args):
        args = args.args
        fmt = profiles.get(args.profile, Formatter)(args.col)

        if args.file is not None:
            with open(args.file, "r", encoding="utf-8") as file:
                for line in file:
                    fmt.match_regex(line)
            return

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
            sys.exit(1)


logging.basicConfig(level=logging.CRITICAL)

COMMAND = Format
