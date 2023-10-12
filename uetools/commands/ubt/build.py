import os
from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import add_arguments, choice
from uetools.args.command import Command, newparser
from uetools.core.conf import (
    engine_folder,
    find_project,
    get_build_modes,
    get_build_platforms,
    guess_platform,
    ubt,
)
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter

project_uht = [
    "UnrealHeaderTool",
    "{PLATFORM}",
    "{MODE}",
    "-Project={UPROJECT}",
    "{UPROJECT}",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-UnrealHeaderTool-{PLATFORM}-{MODE}.txt"',
]

engine_uht = [
    "UnrealHeaderTool",
    "{PLATFORM}",
    "{MODE}",
    "-NoUBTMakefiles"
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml"
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-UnrealHeaderTool-{PLATFORM}-{MODE}.txt"',
]

project_editor = [
    "{PROJECT_NAME}Editor",
    "{PLATFORM}",
    "{MODE}",
    "-Project={UPROJECT}",
    "{UPROJECT}",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-{PROJECT_NAME}Editor-{PLATFORM}-{MODE}.txt"',
]

shader_compile_worker = [
    "ShaderCompileWorker",
    "{PLATFORM}",
    "{MODE}",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-ShaderCompileWorker-{PLATFORM}-{MODE}.txt"',
]

unrealpak = [
    "UnrealPak",
    "{PLATFORM}",
    "{MODE}",
    "-Project={UPROJECT}",
    "{UPROJECT}",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-UnrealPak-{PLATFORM}-{MODE}.txt"',
]

project = [
    "{PROJECT_NAME}",
    "{PLATFORM}",
    "{MODE}",
    "-Project={UPROJECT}",
    "{UPROJECT}",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-{PROJECT_NAME}-{PLATFORM}-{MODE}.txt"',
]

# this is windows only
bootstrap = [
    "BootstrapPackagedGame",
    "{PLATFORM}",
    "Shipping",
    "-NoUBTMakefiles",
    "-Manifest={ENGINE_FOLDER}/Intermediate/Build/Manifest.xml",
    "-NoHotReload",
    '-abslog="{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-BootstrapPackagedGame-{PLATFORM}-Shipping.txt"',
]


# This is the build commands issued by UAT when using BuildCookRun.
build_update_project = [
    project_uht,
    engine_uht,
    project_editor,
    shader_compile_worker,
    unrealpak,
    project,
    bootstrap,
]


short_update = [
    project_editor,
    shader_compile_worker,
]


profiles = {"update-project": build_update_project, "short-update": short_update}


def replace_variables(command, variables):
    """Replace variables in a command"""
    cmd = []
    for arg in command:
        for key, value in variables.items():
            arg = arg.replace(f"{{{key}}}", value)

        cmd.append(arg)
    return cmd


# fmt: off
@dataclass
class Arguments:
    target  : str                        # Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)
    platform: str = choice(*get_build_platforms(), default=guess_platform())  # Platform to build for, defaults to current platform (Win64, Linux, etc..)
    mode    : str = choice(*get_build_modes(), default="Development")  # Build mode (Tests, Debug, Development, Shipping)
    profile : Optional[str] = None  # Build multiple targets using a configuration
# fmt: on


class Build(Command):
    """Execute UnrealBuildTool for a specified target

    Examples
    --------

    .. code-block:: console

       # Builds the Editor for the `RTSGame` project
       # Only run the build editor target
       uecli build RTSGameEditor

       # Runs all the command UAT would execute to compile the project (i.e compiles ShaderCompileWorker and others)
       uecli build RTSGame --profile update-project

    Notes
    -----

    While this works (as of 2022-08-21), you should probably rely epics generated commands instead.
    This was done as an exercice to learn about Unreal internals and might not get updated too often.

    """

    name: str = "build"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Build)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute_profile(args):
        """Execute a command profile"""
        commands = profiles.get(args.profile)

        uproject = find_project(args.target)
        assert uproject is not None, f"Project {args.target} does not exist"

        name = args.target
        if name.endswith("Editor"):
            name = name[0:-6]

        variables = {
            "PLATFORM": args.platform,
            "MODE": args.mode,
            "UPROJECT": uproject,
            "PROJECT_NAME": name,
            "ENGINE_FOLDER": engine_folder(),
        }

        rc = 0
        for command in commands:
            # Temporary fix `BootstrapPackagedGame` is Windows only
            if "BootstrapPackagedGame" in command and args.platform != "Windows":
                continue

            cmd = replace_variables(command, variables)

            cmd = [ubt()] + cmd
            print(" ".join(cmd), flush=True)

            fmt = Formatter()
            rc += popen_with_format(fmt, cmd)

        return rc

    @staticmethod
    def execute(args):
        """Execute the UAT build tool on the target"""
        target = args.target
        platform = args.platform
        mode = args.mode

        if args.profile:
            return Build.execute_profile(args)

        assert target is not None, "Target name is required"
        engine_path = engine_folder()

        logfolder = os.path.join(engine_path, "Programs/AutomationTool/Saved.Logs")
        logfile = f"UBT-{target}-{platform}-{mode}.txt"
        logfile = os.path.join(logfolder, logfile)
        # "{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-UnrealHeaderTool-Win64-Development.txt"

        cmd = [
            target,
            platform,
            mode,
        ]

        # Check if the target is a project
        uproject = find_project(target)

        if uproject is not None:
            cmd += [f"-Project={uproject}", uproject]

        cmd.append("-NoUBTMakefiles")
        cmd.append("-NoHotReload")
        cmd.append(f"-Manifest={engine_path}/Intermediate/Build/Manifest.xml")
        cmd.append(f"-abslog={logfile}")

        # Tools
        #   RequiredTools UnrealFrontend UnrealEditor UnrealInsights
        #
        # I have an issue forwarding arguments to linux
        # The make file simply does:
        #    $(BUILD) UnrealHeaderTool Linux Development  -project="$(GAMEPROJECTFILE)" $(ARGS)
        # with:
        #   bash "$(UNREALROOTPATH)/Engine/Build/BatchFiles/Linux/Build.sh"
        #
        # The script then does:
        #  dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll "$@"
        #
        #
        cmd = [ubt()] + cmd
        print(" ".join(cmd), flush=True)

        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = Build
