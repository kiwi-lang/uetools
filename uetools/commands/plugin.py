import os
from dataclasses import dataclass, field
from typing import List, Optional

from uetools.command import Command, newparser
from uetools.conf import get_build_platforms, load_conf, uat
from uetools.run import run


@dataclass
class Arguments:
    """Builds and cook a plugin"""

    project: str
    plugin: str
    platforms: List[str] = field(default_factory=list)
    output: str = None
    strict_includes: Optional[bool] = None
    no_host_platform: Optional[bool] = None


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

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, project)

        plugin_path = os.path.join(project_folder, plugin)

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
