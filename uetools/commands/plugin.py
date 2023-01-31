import json
import os
import tempfile
from dataclasses import dataclass
from typing import Optional
import shutil

import pkg_resources
from cookiecutter.main import cookiecutter

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import (
    find_project,
    get_build_platforms,
    guess_platform,
    uat,
    get_version_tag,
    engine_folder,
    retrieve_exact_engine_version
)
from uetools.core.run import popen_with_format
from uetools.format.cooking import CookingFormatter


# fmt: off
@dataclass
class Arguments:
    """Builds and cook a plugin"""

    # project             : str # Name of the project
    # plugin              : str # Path to the plugin (relative to project folder)
    # platforms           : List[str] = field(default_factory=list)
    # output              : str  = None  # Packaged plugin destination
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
    EngineDir           : Optional[str] = None  # Engine directory
    CreateSubFolder     : bool = False  # Create a subfolder for the plugin
    NoPCH               : bool = False  # No Precompiled Header
    NoSharedPCH         : bool = False  # No Shared Precompiled Header
    DisableUnity        : bool = False  # Disable Unity Build
    NoDeleteHostProject : bool = False  # Do not delete host project (which was created to prepare the plugin)
    # this does not exist when calling BuildPlugin
    # UbtArgs             : Optional[str]     = None  # extra options to pass to ubt
# fmt: on


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

    name: str = "plugin-cook"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, PackagePlugin)
        parser.add_argument("plugin", type=str, help="Path to uplugin file")
        parser.add_argument(
            "--project", type=str, help="Project name containing the plugin"
        )
        parser.add_argument(
            "--platforms",
            type=str,
            nargs="+",
            choices=get_build_platforms(),
            default=[guess_platform()],
            help="list of platforms to build for",
        )
        parser.add_argument(
            "--output", type=str, help="path to build the packaged plugin"
        )

        parser.add_arguments(Arguments, dest="pkg")

    @staticmethod
    def execute(args):
        project = args.project
        plugin = args.plugin
        platforms = "+".join(args.platforms)

        if project is not None and not os.path.isabs(plugin):
            project = find_project(args.project)
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
                f"-Package={args.output}",
                f"-TargetPlatforms={platforms}",
            ]
            + command_builder(args.pkg)
            + ["-nocompileuat"]
        )

        print(" ".join(cmdargs))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True
        return popen_with_format(fmt, cmdargs)


class NewPlugin(Command):
    """Create a new plugin from a template"""

    name: str = "plugin-new"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, NewPlugin)
        parser.add_argument(
            "project", type=str, help="Project in which the plugin will live"
        )
        parser.add_argument("plugin", type=str, help="Name of the plugin")

    @staticmethod
    def execute(args):
        project = find_project(args.project)
        project_dir = os.path.dirname(project)

        template = pkg_resources.resource_filename(
            __name__, "../templates/PluginTemplate/cookiecutter.json"
        )
        assert os.path.exists(template)
        template = os.path.dirname(template)
        assert os.path.exists(template)

        configfile = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"default_context": {"plugin_name": args.plugin}}, configfile)
        configfile.flush()

        plugin_dir = os.path.join(project_dir, "Plugins")
        assert os.path.exists(plugin_dir)

        kwargs = dict(
            no_input=True,
            config_file=configfile.name,
            overwrite_if_exists=True,
            output_dir=plugin_dir,
        )

        cookiecutter(
            template,
            **kwargs,
        )

        # Windows have permission issues on reading a temporary files
        configfile.close()
        os.remove(configfile.name)


class FinalizePlugin(Command):
    """Finalize Plugin for redistribution
    
    * Set the engine version inside the <plugin>.uplugin
    * Set installed to false inside <plugin>.uplugin
    * Check MarketplaceURL
    * Set VersionName 
    * Copy some Config folder

    """

    name: str = "plugin-finalize"

    @dataclass
    class Arguments:
        plugin: str    # plugin name
        output: str    # output


    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, FinalizePlugin)
        parser.add_arguments(FinalizePlugin.Arguments, dest="args")

    @staticmethod
    def execute(args):
        args = args.args
        base_url = 'com.epicgames.launcher://ue/marketplace/product/'

        plugin_dir = os.path.dirname(args.plugin)
        plugin_version = get_version_tag(plugin_dir).replace("v", "")
        engine_version = retrieve_exact_engine_version(engine_folder())

        # Configure the plugin descriptor
        # -------------------------------
        with open(args.output, "r") as f:
            uplugin = json.load(f)

        uplugin['VersionName'] = plugin_version
        uplugin['Installed'] = False
        uplugin['EngineVersion'] = engine_version
        
        assert len(uplugin['MarketplaceURL'][len(base_url):]) > 0, "MarketPlace URL missing"

        with open(args.output, 'w') as f:
            json.dump(uplugin, f)
        
        # Copy files
        # ----------
        config_folder = os.path.join(plugin_dir, 'Config')
        output_folder = os.path.dirname(args.output)
        
        shutil.copytree(config_folder, os.path.join(output_folder, "Config"))


        

COMMANDS = [PackagePlugin, NewPlugin, FinalizePlugin]
