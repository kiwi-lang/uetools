


import os
import sys
import subprocess

from gamekit.conf import Command, load_conf, uat, get_build_platforms


class PackagePlugin(Command):
    """Builds and cook a plugin"""

    name: str = "plugin"

    @staticmethod
    def arguments(subparsers):
        cook = subparsers.add_parser(PackagePlugin.name, help='Package an UnrealEngine Plugin')
        cook.add_argument("project", type=str, help='Project name')

        cook.add_argument("plugin", type=str, help='Path to uplugin file')

        cook.add_argument("--platforms", type=str, nargs='+', choices=get_build_platforms(),
                          help='list of platforms to build for')

        cook.add_argument("--output", type=str,
                          help='path to build the packaged plugin')

        cook.add_argument("--strict-includes", action='store_true',
                          help='Disables precompiled headers & unity build. (Forces Headers to include all their dependencies)')

        cook.add_argument("--no-host-platform", action='store_true',
                          help='Does not compile the editor platform on the host')

    @staticmethod
    def execute(args):
        project = args.project
        plugin = args.plugin

        projects_folder = load_conf().get('project_path')
        project_folder = os.path.join(projects_folder, project)

        uproject = os.path.join(project_folder, f'{project}.uproject')
        plugin_path = os.path.join(project_folder, plugin)

        platforms = '+'.join(args.platforms)

        cmdargs = [
            uat(),
            "BuildPlugin",

            f"-Plugin={plugin_path}",
            f"-Package={args.output}",
            f"-TargetPlatforms={platforms}",

            # what does this do ?
            '-Rocket'
        ]
        if args.strict_includes:
            cmdargs.append("-StrictIncludes")

        if args.no_host_platform:
            cmdargs.append("-NoHostPlatform ")

        p = subprocess.run(cmdargs,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True
        )

        print(f"Subprocess terminated with (rc: {p.returncode})")
        return


COMMAND = PackagePlugin
