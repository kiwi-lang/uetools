from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import choice
from uetools.args.command import Command, command_builder
from uetools.core.conf import (
    find_project,
    get_build_modes,
    get_build_platforms,
    guess_platform,
    uat,
)
from uetools.core.run import popen_with_format
from uetools.format.cooking import CookingFormatter
from uetools.core.util import deduce_project


class CookGameUAT(Command):
    """Cook your main game using UAT"""

    name: str = "cook"

    # fmt: off
    @dataclass
    class Arguments:
        """Cook arguments for UAT"""

        project         : str = deduce_project()
        unattended      : bool = True
        utf8output      : bool = True
        platform        : str = choice(*get_build_platforms(), default=guess_platform())    # Platform
        clientconfig    : str = choice(*get_build_modes(), default="Development")           # Client Build configuration
        serverconfig    : str = choice(*get_build_modes(), default="Development")           # Server Build configuration
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
