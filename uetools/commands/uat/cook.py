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


from .arguments import BuildCookRunArguments


class CookGameUAT(Command):
    """Cook your main game using UAT"""

    name: str = "cook"

    # fmt: off
    @dataclass
    class Arguments(BuildCookRunArguments): 
        build                                  : bool = True
        
        cook                                   : bool = True
        stage                                  : bool = True

        prereqs                                : bool = True
        distribution                           : bool = True
        pak                                    : bool = True
        
        # client                                 : bool = True
        dedicatedserver                        : bool = True
        servertargetplatform                   : str  = "Win64"
        targetplatform                         : str  = "Win64"

        unattended                             : bool = True
        utf8output                             : bool = True
        noP4                                   : bool = True
        nullrhi                                : bool = True
    # fmt: on


    @staticmethod
    def execute(args):
        assert args.project is not None

        args.project = find_project(args.project)

        uat_args = command_builder(args)
        cmd = [uat()] + ["BuildCookRun"] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True

        returncode = popen_with_format(fmt, cmd, shell=False)
        fmt.summary()

        returncode = 0
        return returncode


COMMANDS = CookGameUAT
