import os
from dataclasses import dataclass
from typing import List, Optional

from argklass.command import Command

from uetools.core.conf import find_project, uat
from uetools.core.options import platform_choices, pluginfield, projectfield
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder
from uetools.format.cooking import CookingFormatter


class PackagePlugin(Command):
    """Builds and cook a plugin

    Examples
    ---------

    Path to a plugin that is not inside a project

    .. code-block:: python

       uetools plugin-cook /Projects/Gamekit/Gamekit.uplugin --output /Built/Gamekit/ --platforms Win64


    Path to a plugin inside a project

    .. code-block:: python

       uetools plugin-cook --project MyHostProject Plugins/Gamekit/Gamekit.uplugin --output /Built/Gamekit/ --platforms Win64

    """

    name: str = "package"

    # fmt: off
    @dataclass
    class Arguments:
        """Builds and cook a plugin"""

        output              : str           = None
        project             : str           = projectfield()    # project's name
        plugin              : str           = pluginfield()     # Plugin's name"
        platforms           : List[str]     = platform_choices()  # List of platforms to build for
        EngineDir           : Optional[str] = None                # Engine directory
        StrictIncludes      : bool = False  # Disables precompiled headers and unity build in order to check all source files have self-contained headers.
        NoHostPlatform      : bool = False  # Prevent compiling for the editor platform on the host
        verbose             : bool = False  # Enables verbose logging
        veryverbose         : bool = False  # Enables very verbose logging
        submit              : bool = False  # Allows UAT command to submit changes
        nosubmit            : bool = False  # Prevents any submit attempts
        np4                 : bool = False  # Disables Perforce functionality
        nonp4               : bool = False  # Enables Perforce functionality
        NoKill              : bool = False  # Does not kill any spawned processes on exit
        Compile             : bool = False  # Force all script modules to be compiled
        NoCompile           : bool = False  # Do not attempt to compile any script modules
        IgnoreBuildRecords  : bool = False  # Ignore build records (Intermediate/ScriptModule/ProjectName.json)
        UseLocalBuildStorage: bool = False  # Allows you to use local storage for your root build storage dir
        WaitForDebugger     : bool = False  # Waits for a debugger to be attached, and breaks once debugger successfully attached.
        Unversioned         : bool = False  # Do not embed the current engine version into the descriptor
        Rocket              : bool = True   # Undocumented argument
        CreateSubFolder     : bool = False  # Create a subfolder for the plugin
        NoPCH               : bool = False  # No Precompiled Header
        NoSharedPCH         : bool = False  # No Shared Precompiled Header
        DisableUnity        : bool = False  # Disable Unity Build
        NoDeleteHostProject : bool = False  # Do not delete host project (which was created to prepare the plugin)
        # this does not exist when calling BuildPlugin
        # UbtArgs             : Optional[str]     = None  # extra options to pass to ubt
    # fmt: on

    @staticmethod
    def execute(args):
        project = vars(args).pop("project")
        plugin = vars(args).pop("plugin")
        platforms = "+".join(vars(args).pop("platforms"))

        if project is not None and not os.path.isabs(plugin):
            project = find_project(project)
            folder = os.path.dirname(project)
            plugin_path = os.path.join(folder, plugin)

        else:
            plugin_path = plugin

        if not os.path.exists(plugin_path):
            raise RuntimeError(f"Could not find {plugin_path}")

        plugin_path = os.path.abspath(plugin_path)

        cmdargs = (
            [
                uat(),
                "BuildPlugin",
                f"-Plugin={plugin_path}",
                f"-Package={vars(args).pop('output')}",
                f"-TargetPlatforms={platforms}",
                "-unattended",
                "-crash",
            ]
            + command_builder(args)
            # + ["-nocompileuat"]
        )

        print(" ".join(cmdargs))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True
        return popen_with_format(fmt, cmdargs)


COMMANDS = PackagePlugin
