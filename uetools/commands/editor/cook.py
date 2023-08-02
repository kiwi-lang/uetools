import os
from argparse import Namespace
from dataclasses import dataclass
from typing import Optional

from uetools.commands.ubt.build import Build
from uetools.core.arguments import add_arguments, choice
from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import (
    build_platform_from_editor,
    editor_cmd,
    find_project,
    get_build_modes,
    get_editor_platforms,
    guess_editor_platform,
)
from uetools.core.run import popen_with_format
from uetools.format.cooking import CookingFormatter


def editor_platforms():
    return choice(*get_editor_platforms(), default=guess_editor_platform())


def build_modes():
    return choice(*get_build_modes(), default=None)


@dataclass
class Arguments:
    # fmt: off
    project         : str                                   # Project Name
    output          : Optional[str] = None                  # Output
    build           : Optional[str] = build_modes()         # Build modes
    platform        : Optional[str] = editor_platforms()    # Platform to cookf
    compressed      : bool          = True                  # Compressed
    cookall         : bool          = True                  # Cook All the content
    unversioned     : bool          = True                  # unversioned
    WarningsAsErrors: bool          = True                  # Fail on warnings
    # fmt: on


class CookGame(Command):
    """Cook your main game

    Notes
    -----

    UAT builds the game before executing the cook command;  You should too.

    Examples
    --------

    .. code-block:: console

       # Only cooks the game
       uecli cook RTSGame --platform Windows

       # Build the project for development before Cooking
       uecli cook RTSGame --platform Windows --build Development

    """

    name: str = "cook"

    @staticmethod
    def arguments(subparsers):
        """Add arguments to the parser"""
        parser = newparser(subparsers, CookGame)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute(args):
        """Execute the cook command using the editor"""

        name = vars(args).pop("project")
        platform = vars(args).pop("platform")
        build = vars(args).pop("build")

        if build:
            build_args = Namespace()
            build_args.target = name
            build_args.platform = build_platform_from_editor(platform)
            build_args.mode = build
            build_args.profile = "update-project"
            Build.execute_profile(build_args)

        uproject = find_project(name)
        folder = os.path.dirname(uproject)

        if args.output is None:
            args.output = os.path.join(folder, "Saved", "StagedBuilds")

        cli_cmd = [
            "-CrashForUAT",
            "-unattended",
            "-NoLogTimes",
            "-UTF8Output",
            "-FullStdOutLogOutput",
        ]

        options = command_builder(args)

        cmd = (
            [
                editor_cmd(),
                uproject,
                "-run=cook",
                f"-targetplatform={platform}",
                f"-abslog={folder}/Saved/Automation/Cooking.txt",
            ]
            + cli_cmd
            + options
        )

        print(" ".join(cmd), flush=True)

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd)
        fmt.summary()

        print(f"Subprocess terminated with (rc: {returncode})")
        return returncode


COMMANDS = [
    CookGame,
]
