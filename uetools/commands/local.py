import os
import subprocess
from dataclasses import dataclass
from typing import Optional

import pkg_resources
from simple_parsing import choice

from uetools.command import Command, command_builder
from uetools.conf import editor_cmd, load_conf

actions = ["Gather", "Compile", "import", "export"]


@dataclass
class ArgumentsUAT:
    """Generate localization files"""

    name: str
    action: choice(*actions)


class LocalUAT(Command):
    """TODO"""

    @staticmethod
    def arguments(subparsers):
        pass

    @staticmethod
    def execute(args):
        pass


# fmt: off
@dataclass
class ArgumentEditor:
    """Generate localization files for your unreal project

    Examples
    --------

    .. code-block:: console

       uecli local --project RTSGame --run GatherText --target RTSGame

    """
    project                 : str # Project we are generating localization for
    run                     : str = choice(["GatherText"], default='GatherText')
    target                  : Optional[str] = None # Localization target (defaults to the project name)
    SCCProvider             : Optional[str] = None # Source control provider
    EnableSCC               : bool = False # enable source control
    DisableSCCSubmit        : bool = True # Disable submitting to source control
    Unattended              : bool = True # Don't ask for user input
    NoShaderCompile         : bool = True # Prevent shader compilation
    multiprocess            : bool = True # Use multiple threads to gather text
    ReportStaleGatherCache  : bool = False # Generates a StaleGatherCacheReport.txt file alongside the manifest for your localization target. This file contains a list of any Assets that contain a stale gather cache.
    FixStaleGatherCache     : bool = False # Attempts to automatically fix any Assets that contain a stale gather cache, by re-saving them.
    FixMissingGatherCache   : bool = False # For Assets too old to have a gather cache, this attempts to automatically fix Assets that are missing a gather cache by re-saving them.
# fmt: on


class LocalEditor(Command):
    """Generate localization files using unreal editor"""

    name: str = "local"

    @staticmethod
    def arguments(subparsers):
        """Localization arguments"""
        init = subparsers.add_parser(
            LocalEditor.name, help="Initialize engine location"
        )
        init.add_arguments(ArgumentEditor, dest="args")
        init.add_argument(
            "--bootstrap",
            action="store_true",
            default=False,
            help="Generate default Localization configuration for your project",
        )

    @staticmethod
    def bootstrap(name, target):
        """Bootstrap localization configuration for your project"""
        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, name)

        localization_config = os.path.join(project_folder, "Config", "Localization")
        os.makedirs(localization_config, exist_ok=True)

        template = pkg_resources.resource_filename(
            __name__, "../templates/Localization/TargetName.ini"
        )

        with open(template, "r", encoding="utf-8") as template:
            template = template.read()

        template.replace("{TargetName}", name)

        with open(
            os.path.join(localization_config, f"{target}.ini"), "w", encoding="utf-8"
        ) as file:
            file.write(template)

    @staticmethod
    def execute(args):
        """Execute localization gathering"""
        name = args.args.project
        target = args.args.target or name

        if args.bootstrap:
            LocalEditor.bootstrap(name, target)

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, name)
        uproject = os.path.join(project_folder, f"{name}.uproject")

        cmd = [
            editor_cmd(),
            uproject,
            f"-config={project_folder}/Config/Localization/{target}.ini",
        ] + command_builder(args)

        print(" ".join(cmd))
        subprocess.run(
            cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True
        )


COMMAND = LocalEditor
