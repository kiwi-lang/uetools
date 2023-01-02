import os
from dataclasses import asdict, dataclass
from typing import Optional

import pkg_resources
from simple_parsing import choice

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import editor_cmd, find_project, uat
from uetools.core.run import popen_with_format, run
from uetools.format.base import Formatter

actions = ["Gather", "Compile", "import", "export"]


# fmt: off
@dataclass
class ArgumentEditor:
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
    project                 : str  # Project we are generating localization for
    run                     : str = choice(["GatherText"], default='GatherText')
    target                  : Optional[str] = None  # Localization target (defaults to the project name)
    SCCProvider             : Optional[str] = None  # Source control provider
    EnableSCC               : bool = False  # enable source control
    DisableSCCSubmit        : bool = True   # Disable submitting to source control
    Unattended              : bool = True   # Don't ask for user input
    NoShaderCompile         : bool = True   # Prevent shader compilation
    multiprocess            : bool = True   # Use multiple threads to gather text
    ReportStaleGatherCache  : bool = False  # Generates a StaleGatherCacheReport.txt file alongside the manifest for your localization target. This file contains a list of any Assets that contain a stale gather cache.
    FixStaleGatherCache     : bool = False  # Attempts to automatically fix any Assets that contain a stale gather cache, by re-saving them.
    FixMissingGatherCache   : bool = False  # For Assets too old to have a gather cache, this attempts to automatically fix Assets that are missing a gather cache by re-saving them.
# fmt: on


class LocalEditor(Command):
    """Generate localization files using unreal editor"""

    name: str = "local"

    @staticmethod
    def arguments(subparsers):
        """Localization arguments"""
        parser = newparser(subparsers, LocalEditor)
        parser.add_arguments(ArgumentEditor, dest="args")
        parser.add_argument(
            "--bootstrap",
            action="store_true",
            default=False,
            help="Generate default Localization configuration for your project",
        )

    @staticmethod
    def bootstrap(name, target):
        """Bootstrap localization configuration for your project"""
        project = find_project(name)
        folder = os.path.dirname(project)

        localization_config = os.path.join(folder, "Config", "Localization")
        os.makedirs(localization_config, exist_ok=True)

        template = pkg_resources.resource_filename(
            __name__, "../templates/Localization/TargetName.ini"
        )

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
        name = args.args.project
        target = args.args.target or name

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

        print(" ".join(cmd))
        return run(cmd, check=True).returncode


# fmt: off
@dataclass
class UATArguments:
    """Updates the external localization data using the arguments provided.

    Attributes
    ----------
    project: str
        Project name

    UEProjectRoot: Optional[str]
        Optional root-path to the project we're gathering for (defaults to CmdEnv.LocalRoot if unset).

    UEProjectDirectory: str
        Sub-path to the project we're gathering for (relative to UEProjectRoot)

    UEProjectName: Optional[str]
        Optional name of the project we're gathering for (should match its .uproject file, eg QAGame).

    LocalizationProjectNames: Optional[str]
        Comma separated list of the projects to gather text from.

    LocalizationBranch: Optional[str]
        Optional suffix to use when uploading the new data to the localization provider.

    LocalizationProvider: Optional[str]
        Optional localization provide override.

    LocalizationSteps: Optional[str]
        Optional comma separated list of localization steps to perform [Download, Gather, Import, Export, Compile, GenerateReports, Upload] (default is all). Only valid for projects using a modular config.

    IncludePlugins: bool
        Optional flag to include plugins from within the given UEProjectDirectory as part of the gather. This may optionally specify a comma separated list of the specific plugins to gather (otherwise all plugins will be gathered).

    ExcludePlugins: Optional[str]
        Optional comma separated list of plugins to exclude from the gather.

    IncludePlatforms: bool
        Optional flag to include platforms from within the given UEProjectDirectory as part of the gather.

    AdditionalCSCommandletArguments: Optional[str]
        Optional arguments to pass to the gather process.

    ParallelGather: bool
        Run the gather processes for a single batch in parallel rather than sequence.

    OneSkyProjectGroupName: Optional[str] = None

    Examples
    --------

    .. code-block:: console

       uecli uat-local --project GamekitDev --IncludePlugins --ParallelGather --LocalizationSteps Gather --LocalizationProjectNames GamekitDev

    """

    project                         : str                    # Project name
    UEProjectRoot                   : Optional[str] = None   # Optional root-path to the project we're gathering for (defaults to CmdEnv.LocalRoot if unset).
    UEProjectDirectory              : str           = ''     # Sub-path to the project we're gathering for (relative to UEProjectRoot).
    UEProjectName                   : Optional[str] = None   # Optional name of the project we're gathering for (should match its .uproject file, eg QAGame).
    LocalizationProjectNames        : Optional[str] = None   # Comma separated list of the projects to gather text from.
    LocalizationBranch              : Optional[str] = None   # Optional suffix to use when uploading the new data to the localization provider.
    LocalizationProvider            : Optional[str] = None   # Optional localization provide override."
    LocalizationSteps               : Optional[str] = None   # Optional comma separated list of localization steps to perform [Download, Gather, Import, Export, Compile, GenerateReports, Upload] (default is all). Only valid for projects using a modular config.
    IncludePlugins                  : bool          = False  # Optional flag to include plugins from within the given UEProjectDirectory as part of the gather. This may optionally specify a comma separated list of the specific plugins to gather (otherwise all plugins will be gathered).
    ExcludePlugins                  : Optional[str] = None   # Optional comma separated list of plugins to exclude from the gather.
    IncludePlatforms                : bool          = False  # Optional flag to include platforms from within the given UEProjectDirectory as part of the gather.
    AdditionalCSCommandletArguments : Optional[str] = None   # Optional arguments to pass to the gather process.
    ParallelGather                  : bool          = False  # Run the gather processes for a single batch in parallel rather than sequence.
    OneSkyProjectGroupName          : Optional[str] = None
# fmt: on


class LocalUAT(Command):
    """Use the UAT to run localization gathering"""

    name: str = "uat-local"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, LocalUAT)
        parser.add_arguments(UATArguments, dest="local")

    @staticmethod
    def execute(args):
        args.local.project = find_project(args.local.project)

        if args.local.UEProjectRoot is None:
            args.local.UEProjectRoot = os.path.dirname(args.local.project)

        if args.local.UEProjectName is None:
            args.local.UEProjectName = os.path.basename(args.local.UEProjectRoot)

        args = asdict(args.local)

        uat_args = command_builder(args)
        cmd = [uat()] + ["Localize"] + uat_args

        print(" ".join(cmd))

        fmt = Formatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd)
        fmt.summary()

        return returncode


COMMANDS = [
    LocalEditor,
    LocalUAT,
]
