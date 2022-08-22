import os
import subprocess

from uetools.conf import (
    Command,
    get_build_modes,
    get_build_platforms,
    guess_platform,
    load_conf,
    ubt,
)

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

profiles = {
    "update-project": build_update_project,
}


def is_project(target):
    """Return true if the target was inferred to be a project name"""
    if target.endswith("Editor"):
        target = target[0:-6]

    projects_folder = load_conf().get("project_path")
    project_folder = os.path.join(projects_folder, target)
    uproject = os.path.join(project_folder, f"{target}.uproject")
    return os.path.exists(uproject), uproject


def replace_variables(command, variables):
    """Replace variables in a command"""
    cmd = []
    for arg in command:
        for key, value in variables.items():
            arg = arg.replace(f"{{{key}}}", value)

        cmd.append(arg)
    return cmd


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
        build = subparsers.add_parser(Build.name, help="Run Unreal Build Tool (UBT)")
        build.add_argument("target", type=str, help="Target name")
        build.add_argument(
            "--platform",
            type=str,
            default=guess_platform(),
            help="Platform to build for",
            choices=set(list(get_build_platforms())),
        )
        build.add_argument(
            "--mode",
            type=str,
            default="Development",
            help="Build mode",
            choices=list(get_build_modes()),
        )
        build.add_argument(
            "--profile",
            type=str,
            default=None,
            help="Build multiple targets using a configuration",
        )

    @staticmethod
    def execute_profile(args):
        """Execute a command profile"""
        commands = profiles.get(args.profile)

        exists, uproject = is_project(args.target)
        assert exists, f"Project {args.target} does not exist"

        name = args.target
        if name.endswith("Editor"):
            name = name[0:-6]

        variables = {
            "PLATFORM": args.platform,
            "MODE": args.mode,
            "UPROJECT": uproject,
            "PROJECT_NAME": name,
            "ENGINE_FOLDER": load_conf().get("engine_path"),
        }

        for command in commands:
            # Temporary fix `BootstrapPackagedGame` is Windows only
            if "BootstrapPackagedGame" in command and args.platform != "Windows":
                continue

            cmd = replace_variables(command, variables)

            cmd = [ubt()] + cmd
            print(" ".join(cmd), flush=True)
            subprocess.run(cmd, check=True)

    @staticmethod
    def execute(args):
        target = args.target
        platform = args.platform
        mode = args.mode

        if args.profile:
            Build.execute_profile(args)
            return

        assert target is not None, "Target name is required"
        engine_path = load_conf().get("engine_path")

        logfolder = os.path.join(engine_path, "Programs/AutomationTool/Saved.Logs")
        logfile = f"UBT-{target}-{platform}-{mode}.txt"
        logfile = os.path.join(logfolder, logfile)
        # "{ENGINE_FOLDER}/Programs/AutomationTool/Saved/Logs/UBT-UnrealHeaderTool-Win64-Development.txt"

        args = [
            target,
            platform,
            mode,
        ]

        # Check if the target is a project
        exists, uproject = is_project(target)
        if exists:
            args += [f"-Project={uproject}", uproject]

        args.append("-NoUBTMakefiles")
        args.append("-NoHotReload")
        args.append(f"-Manifest={engine_path}/Intermediate/Build/Manifest.xml")
        args.append(f"-abslog={logfile}")

        # Tools
        #    RequiredTools UnrealFrontend UnrealEditor UnrealInsights
        #
        # I have an issue forwarding arguments to linux
        # The make file simply does:
        #     $(BUILD) UnrealHeaderTool Linux Development  -project="$(GAMEPROJECTFILE)" $(ARGS)
        # with:
        #    bash "$(UNREALROOTPATH)/Engine/Build/BatchFiles/Linux/Build.sh"
        #
        # The script then does:
        #   dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll "$@"
        #
        #
        cmd = [ubt()] + args
        print(" ".join(cmd), flush=True)

        subprocess.run(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


COMMAND = Build
