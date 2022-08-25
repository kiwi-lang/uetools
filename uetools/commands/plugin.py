import os
from dataclasses import dataclass, field
from typing import List

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project, get_build_platforms, uat
from uetools.core.run import run


# fmt: off
@dataclass
class Arguments:
    """Builds and cook a plugin"""

    project         : str # Name of the project
    plugin          : str # Path to the plugin (relative to project folder)
    platforms       : List[str] = field(default_factory=list)
    output          : str       = None  # Packaged plugin destination
    strict_includes : bool      = False #
    no_host_platform: bool      = False #
# fmt: on


class PackagePlugin(Command):
    """Builds and cook a plugin"""

    name: str = "plugin"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, PackagePlugin)
        parser.add_argument("project", type=str, help="Project name")

        parser.add_argument("plugin", type=str, help="Path to uplugin file (relative)")

        parser.add_argument(
            "--platforms",
            type=str,
            nargs="+",
            choices=get_build_platforms(),
            help="list of platforms to build for",
        )

        parser.add_argument(
            "--output", type=str, help="path to build the packaged plugin"
        )

        parser.add_argument(
            "--strict-includes",
            action="store_true",
            help="Disables precompiled headers & unity build. (Forces Headers to include all their dependencies)",
        )

        parser.add_argument(
            "--no-host-platform",
            action="store_true",
            help="Does not compile the editor platform on the host",
        )

    @staticmethod
    def execute(args):
        project = args.project
        plugin = args.plugin

        project = find_project(args.project)
        folder = os.path.dirname(project)

        print()
        print(args.project, project)
        print(folder)
        print()

        plugin_path = os.path.join(folder, plugin)

        platforms = "+".join(args.platforms)

        cmdargs = [
            uat(),
            "BuildPlugin",
            f"-Plugin={plugin_path}",
            f"-Package={args.output}",
            f"-TargetPlatforms={platforms}",
            # what does this do ?
            "-Rocket",
        ]

        if args.strict_includes:
            cmdargs.append("-StrictIncludes")

        if args.no_host_platform:
            cmdargs.append("-NoHostPlatform ")

        print(" ".join(cmdargs))
        run(
            cmdargs,
            check=True,
        )


COMMANDS = PackagePlugin
