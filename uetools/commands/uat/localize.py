import os
from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import find_project, uat
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder, deduce_project
from uetools.format.base import Formatter

actions = ["Gather", "Compile", "import", "export"]


class LocalUAT(Command):
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

    name: str = "localize"

    # fmt: off
    @dataclass
    class Arguments:
        project                         : str = deduce_project() # Project name
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

    @staticmethod
    def execute(args):
        args.project = find_project(args.project)

        if args.UEProjectRoot is None:
            args.UEProjectRoot = os.path.dirname(args.project)

        if args.UEProjectName is None:
            args.UEProjectName = os.path.basename(args.UEProjectRoot)

        uat_args = command_builder(args)
        cmd = [uat()] + ["Localize"] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = Formatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd)
        fmt.summary()

        return returncode


COMMANDS = [
    LocalUAT,
]
