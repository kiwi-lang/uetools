import os
import sys
from argparse import Namespace
from dataclasses import dataclass
from typing import Optional

from simple_parsing import choice

from uetools.command import Command, command_builder
from uetools.commands.build import Build
from uetools.conf import (
    build_platform_from_editor,
    editor_cmd,
    find_project,
    get_build_modes,
    get_editor_platforms,
    guess_editor_platform,
    load_conf,
)
from uetools.format.base import popen_with_format
from uetools.format.cooking import CookingFormatter


@dataclass
class Arguments:
    """Cook your main game

    Attributes
    ----------
    name: str
        Name of the project to cook

    output: str
        Cooking result output path, defaults to ``$PROJECT_NAME/Saved/StagedBuilds/``

    build: str
        Build mode, if set a build command will be issued before cooking

    platform: str
        Used if build mode is set.

    compressed: bool
        Compress the cooked data, defaults to ``True``

    cookall: bool
        Cook all assets, defaults to ``False``

    unversioned: bool
        Don't version the cooked data, defaults to ``False``

    WarningsAsErrors: bool
        Treat warnings as errors, defaults to ``False``

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

    project: str
    output: Optional[str] = None
    build: Optional[str] = choice(*get_build_modes(), default=None)
    platform: Optional[str] = choice(
        *get_editor_platforms(), default=guess_editor_platform()
    )
    compressed: bool = True
    cookall: bool = True
    unversioned: bool = True
    WarningsAsErrors: bool = True


class CookGame(Command):
    """Cook your main game"""

    name: str = "cook"

    @staticmethod
    def arguments(subparsers):
        cook = subparsers.add_parser(
            CookGame.name, help="Run Unreal Automation Test (UAT)"
        )
        cook.add_arguments(Arguments, dest="cook")

    @staticmethod
    def execute(args):
        CookGame.execute_editor(args)

    @staticmethod
    def execute_editor(args):
        """Execute the cook command using the editor"""
        # UAT just uses the editor at the end anyway
        args = args.cook

        name = vars(args).pop("project")
        platform = vars(args).pop("platform")
        build = vars(args).pop("build")
        if build:
            build_args = Namespace()
            build_args.target = name
            build_args.platform = build_platform_from_editor(platform)
            build_args.mode = args.build
            build_args.profile = "update-project"
            Build.execute_profile(build_args)

        uproject = find_project(name)

        if args.output is None:
            project_folder = load_conf().get("project_folder")
            args.output = os.path.join(project_folder, "Saved", "StagedBuilds")

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
                f"-abslog={project_folder}/Saved/Automation/Cooking.txt",
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

        if returncode != 0:
            sys.exit(returncode)


COMMAND = CookGame
