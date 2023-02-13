from dataclasses import dataclass
from typing import Optional

from uetools.core.arguments import add_arguments, choice
from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import (
    find_project,
    get_build_modes,
    get_build_platforms,
    guess_platform,
    uat,
)
from uetools.core.run import popen_with_format
from uetools.format.cooking import CookingFormatter


# fmt: off
@dataclass
class UATArguments:
    """Cook arguments for UAT"""

    project         : str
    unattended      : bool = True
    utf8output      : bool = True
    platform        : str = choice(*get_build_platforms(), default=guess_platform())    #: Platform
    clientconfig    : str = choice(*get_build_modes(), default="Development")           #: Client Build configuration
    serverconfig    : str = choice(*get_build_modes(), default="Development")           #: Server Build configuration
    noP4            : bool = True
    nodebuginfo     : bool = True
    allmaps         : bool = True
    cook            : bool = True
    build           : bool = True
    stage           : bool = True
    prereqs         : bool = True
    pak             : bool = True
    archive         : bool = True
    stagingdirectory: Optional[str] = None
    archivedirectory: Optional[str] = None
    WarningsAsErrors: bool = True


# fmt: on


class CookGameUAT(Command):
    """Cook your main game using UAT"""

    name: str = "cook"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, CookGameUAT)
        add_arguments(parser, UATArguments)

    @staticmethod
    def execute(args):
        args.project = find_project(args.project)

        uat_args = command_builder(args)
        cmd = [uat()] + ["BuildCookRun"] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd, shell=False)
        fmt.summary()

        return returncode


COMMANDS = CookGameUAT
