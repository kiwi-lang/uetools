import os
from dataclasses import dataclass
from typing import Optional

from argklass.arguments import choice
from argklass.cache import load_resource
from argklass.command import Command

from uetools.core.conf import editor_cmd, find_project
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder, deduce_project
from uetools.format.base import Formatter

actions = ["Gather", "Compile", "import", "export"]


class LocalEditor(Command):
    """Generate localization files for your unreal project

    Attributes
    ----------

    project: str
        Project we are generating localization for

    run: str
        Name of the localization commandlet to run

    target: str
        Localization target (defaults to the project name)

    SCCProvider: bool
        Source control provider

    EnableSCC: bool
        enable source control

    DisableSCCSubmit: bool
        Disable submitting to source control

    Unattended: bool
        Don't ask for user input

    NoShaderCompile: bool
        Prevent shader compilation

    multiprocess: bool
        Use multiple threads to gather text

    ReportStaleGatherCache: bool
        Generates a StaleGatherCacheReport.txt file alongside the manifest for your localization target. This file contains a list of any Assets that contain a stale gather cache.

    FixStaleGatherCache: bool
        Attempts to automatically fix any Assets that contain a stale gather cache, by re-saving them.

    FixMissingGatherCache: bool
        For Assets too old to have a gather cache, this attempts to automatically fix Assets that are missing a gather cache by re-saving them.

    Examples
    --------

    .. code-block:: console

       uecli local --project RTSGame --run GatherText --target RTSGame
    """

    name: str = "localize"

    # fmt: off
    @dataclass
    class Arguments:
        project                 : Optional[str] = deduce_project()  # Name of the the project to open
        run                     : str = choice(*actions, default="GatherText")
        target                  : Optional[str] = None  # Localization target (defaults to the project name)
        SCCProvider             : Optional[str] = None  # Source control provider
        EnableSCC               : bool = False  # enable source control
        DisableSCCSubmit        : bool = True   # Disable submitting to source control
        Unattended              : bool = True   # Don't ask for user input
        NoShaderCompile         : bool = True   # Prevent shader compilation
        multiprocess            : bool = True   # Use multiple threads to gather text
        ReportStaleGatherCache  : bool = False  # Generates a StaleGatherCacheReport.txt file alongside the manifest for your localization target. This file contains a list of any Assets that contain a stale gather cache.
        FixStaleGatherCache     : bool = False  # Attempts to automatically fix any Assets that contain a stale gather cache, by re-saving them.
        FixMissingGatherCache   : bool = False  # For Assets too old to have a gather cache, this attempts to automatically fix Assets that are missing a gather cache by re-saving them.# fmt: on
        bootstrap               : bool = False  # Generate default Localization configuration for your project
    # fmt: on

    @staticmethod
    def bootstrap(name, target):
        """Bootstrap localization configuration for your project"""
        project = find_project(name)
        folder = os.path.dirname(project)

        localization_config = os.path.join(folder, "Config", "Localization")
        os.makedirs(localization_config, exist_ok=True)

        template = load_resource(__name__, "templates/Localization/TargetName.ini")

        with open(template, encoding="utf-8") as template:
            template = template.read()

        template = template.replace("{TargetName}", name)

        with open(
            os.path.join(localization_config, f"{target}.ini"), "w", encoding="utf-8"
        ) as file:
            file.write(template)

    @staticmethod
    def execute(args):
        """Execute localization gathering"""
        name = vars(args).pop("project")
        target = vars(args).pop("target") or name

        bootstrap = vars(args).pop("bootstrap")
        if bootstrap:
            LocalEditor.bootstrap(name, target)

        project = find_project(name)
        folder = os.path.dirname(project)

        cmd = [
            editor_cmd(),
            project,
            f"-config={folder}/Config/Localization/{target}.ini",
        ] + command_builder(args)

        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = LocalEditor
