
from argparse import Namespace
import os
import sys

from gamekit.conf import LINUX
from gamekit.conf import Command, load_conf, guess_platform, editor_cmd, get_editor_platforms, get_build_modes, build_platform_from_editor
from gamekit.commands.fmt import CookingFormater, popen_with_format
from gamekit.commands.build import Build


class CookGame(Command):
    """Builds and cook your main game

    Notes
    -----

    UAT builds the game before executing the cook command;
    You should too.

    Examples
    --------

    .. code-block:: console

       # Only cooks the game
       gkcli cook GamekitDev --platform Windows

       # Build the project for development before Cooking
       gkcli cook GamekitDev --platform Windows --build Development

    """

    name: str = "cook"

    @staticmethod
    def arguments(subparsers):
        cook = subparsers.add_parser(CookGame.name, help='Run Unreal Automation Test (UAT)')
        cook.add_argument("name", type=str, help='Project name')
        cook.add_argument("--build", default=None,type=str, choices=get_build_modes(), help='builds the project before cooking')
        cook.add_argument("--platform", type=str, default=guess_platform(), help='Platform to build for', choices=set(list(get_editor_platforms())))
        cook.add_argument("--output", type=str, default=None, help='path to build the packaged plugin')

    @staticmethod
    def execute(args):
        CookGame.execute_editor(args)

    @staticmethod
    def execute_editor(args):
        # UAT just uses the editor at the end anyway
        name = args.name
        platform = args.platform

        if args.build:
            build_args = Namespace()
            build_args.target = name
            build_args.platform = build_platform_from_editor(platform)
            build_args.mode = args.build
            build_args.profile = 'update-project'
            Build.execute_profile(build_args)

        projects_folder = load_conf().get('project_path')
        project_folder = os.path.join(projects_folder, name)
        uproject = os.path.join(project_folder, f'{name}.uproject')

        args = [
            uproject,
            '-run=cook',
            f'-targetplatform={platform}',

            '-Compressed',
            '-CookAll',
            # '-log',

            # extracted from a UAT run
            # '-fileopenlog',
            '-unversioned',
            f'-abslog={project_folder}/Saved/Automation/Cooking.txt',

            '-CrashForUAT',
            '-unattended',
            '-NoLogTimes',
            '-UTF8Output',
            '-stdout',
            '-FullStdOutLogOutput',

            # '-map={}'
            # Incremental cooking
            # '-iterate',
            # '-UnVersioned'

            # Command line just disable everything
            '-Unattended',
            '-NullRHI',
            '-NoSplash',
            '-NoSound',
            '-NoPause',
            "-WarningsAsErrors",
        ]

        fmt = CookingFormater(24)
        fmt.print_non_matching = True

        cmd = [editor_cmd()] + args

        print(' '.join(cmd), flush=True)
        returncode = popen_with_format(fmt, cmd)

        fmt.summary()

        print(f"Subprocess terminated with (rc: {returncode})")

        if returncode != 0:
            sys.exit(returncode)

        return

COMMAND = CookGame



