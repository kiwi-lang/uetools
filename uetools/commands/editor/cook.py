import os
from argparse import Namespace
from dataclasses import dataclass
from typing import Optional

from argklass.arguments import choice
from argklass.command import Command

from uetools.commands.ubt.build import Build
from uetools.core.conf import (
    build_platform_from_editor,
    editor_cmd,
    find_project,
    get_build_modes,
    get_editor_platforms,
    guess_editor_platform,
)
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder, deduce_project
from uetools.format.cooking import CookingFormatter


def editor_platforms():
    return choice(*get_editor_platforms(), default=guess_editor_platform())


def build_modes():
    return choice(*get_build_modes(), default=None)


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

    @dataclass
    class Arguments:
        # fmt: off
        project         : Optional[str] = deduce_project()      # Name of the the project to open
        output          : Optional[str] = None                  # Output
        build           : Optional[str] = build_modes()         # Build modes
        platform        : Optional[str] = editor_platforms()    # Platform to cookf
        compressed      : bool          = True                  # Compressed
        cookall         : bool          = True                  # Cook All the content
        unversioned     : bool          = True                  # unversioned
        WarningsAsErrors: bool          = True                  # Fail on warnings
        # fmt: on

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
