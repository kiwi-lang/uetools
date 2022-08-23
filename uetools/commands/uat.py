from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Optional

from uetools.command import Command, command_builder
from uetools.conf import get_build_modes, uat

commands = [
    "AnalyzeThirdPartyLibs",
    "BenchmarkBuild",
    "BenchmarkOptions",
    "BuildCMakeLib",
    "BuildCommonTools",
    "BuildCookRun",
    "BuildDerivedDataCache",
    "BuildEditor",
    "BuildGame",
    "BuildHlslcc",
    "BuildPhysX",
    "BuildPlugin",
    "BuildServer",
    "BuildTarget",
    "BuildThirdPartyLibs",
    "CheckBalancedMacros",
    "CheckCsprojDotNetVersion",
    "CheckForHacks",
    "CheckPerforceCase",
    "CheckRestrictedFolders",
    "CheckTargetExists",
    "CheckXcodeVersion",
    "CleanAutomationReports",
    "CleanFormalBuilds",
    "CopySharedCookedBuild",
    "CopyUAT",
    "CreateComponentZips",
    "CreatePlatformExtension",
    "CryptoKeys",
    "DownloadJupiterBuild",
    "ExportMcpTemplates",
    "ExtractPaks",
    "FinalizeInstalledBuild",
    "FixPerforceCase",
    "FixupRedirects",
    "GenerateDSYM",
    "GeneratePlatformReport",
    "IPhonePackager",
    "ListMobileDevices",
    "ListThirdPartySoftware",
    "Localise",
    "Localize",
    "MegaXGE",
    "MemreportHelper",
    "OpenEditor",
    "ParseMsvcTimingInfo",
    "RebuildHLOD",
    "RebuildLightMaps",
    "RecordPerformance",
    "ReplaceAssetsUsingManifest",
    "ResavePackages",
    "StashTarget",
    "SyncBinariesFromUGS",
    "SyncDDC",
    "SyncDepotPath",
    "SyncProject",
    "UnrealBuildUtilDummyBuildCommand",
    "UnstashTarget",
    "UpdateLocalVersion",
    "UploadDDCToAWS",
    "WorldPartitionBuilder",
    "ZipProjectUp",
    "ZipUtils",
    "P4WriteConfig",
    "Build",
    "BuildGraph",
    "CleanTempStorage",
    "TempStorageTests",
    "MakeCookedEditor",
    "CleanDevices",
    "PublishUnrealAutomationTelemetry",
    "RunEditorTests",
    "RunUnreal",
    "RunUnrealTests",
    "TestGauntlet",
    "ExportIPAFromArchive",
    "MakeIPA",
    "WriteIniValueToPlist",
    "LowLevelTests.Automation",
    "RunLowLevelTests",
    "Turnkey",
]

# fmt: off
@dataclass
class UATArgs:
    """Common UAT arguments"""
    project                 : str  # Project path (required), i.e: -project=QAGame, -project=Samples/BlackJack/BlackJack.uproject, -project=D:/Projects/MyProject.uproject,
    verbose                 : bool = False # Enables verbose logging
    veryverbose             : bool = False # Enables very verbose logging
    submit                  : bool = False # Allows UAT command to submit changes
    nosubmit                : bool = False # Prevents any submit attempts
    nop4                    : bool = False # Disables Perforce functionality {default if not run on a build machine}
    p4                      : bool = False # Enables Perforce functionality {default if run on a build machine}
    list                    : bool = False # Lists all available commands
    nokill                  : bool = False # Does not kill any spawned processes on exit
    compile                 : bool = False # Force all script modules to be compiled
    nocompile               : bool = False # Do not attempt to compile any script modules - attempts to run with whatever is up to date
    ignorebuildrecords      : bool = False # Ignore build records (Intermediate/ScriptModule/ProjectName.json) files when determining if script modules are up to date
    uselocalbuildstorage    : bool = False # Allows you to use local storage for your root build storage dir {default of P:\Builds {on PC} is changed to Engine\Saved\LocalBuilds}. Used for local testing.
    waitfordebugger         : bool = False # Waits for a debugger to be attached, and breaks once debugger successfully attached.
    # help                  : bool = False # Displays help

@dataclass
class BuildCookRunArgs:
    """Arguments for BuildCookRun command"""
    destsample              : bool = False # Destination Sample name),
    foreigndest             : bool = False # Foreign Destination
    targetplatform          : bool = False # target platform for building, cooking and deployment (also -Platform)
    servertargetplatform    : bool = False # target platform for building, cooking and deployment of the dedicated server (also -ServerPlatform)
    foreign                 : bool = False # Generate a foreign uproject from blankproject and use that
    foreigncode             : bool = False # Generate a foreign code uproject from platformergame and use that
    crashreporter           : bool = False # true if we should build crash reporter
    cook                    : bool = False # cookonthefly Determines if the build is going to use cooked data
    skipcook                : bool = False # use a cooked build, but we assume the cooked data is up to date and where it belongs, implies -cook
    skipcookonthefly        : bool = False # in a cookonthefly build, used solely to pass information to the package step
    clean                   : bool = False # wipe intermediate folders before building
    unattended              : bool = False # assumes no operator is present, always terminates without waiting for something.
    pak                     : bool = False # generate a pak file
    iostore                 : bool = False # generate I/O store container file(s)
    cook4iostore            : bool = False # generate I/O store container file(s)
    zenstore                : bool = False # save cooked output data to the Zen storage server
    makebinaryconfig        : bool = False # generate optimized config data during staging to improve loadtimes
    signpak                 : bool = False # sign the generated pak file with the specified key, i.e. -signpak=C:/Encryption.keys. Also implies -signedpak.
    prepak                  : bool = False # attempt to avoid cooking and instead pull pak files from the network, implies pak and skipcook
    signed                  : bool = False # the game should expect to use a signed pak file.
    PakAlignForMemoryMapping: bool = False # The game will be set up for memory mapping bulk data.
    skippak                 : bool = False # use a pak file, but assume it is already built, implies pak
    skipiostore             : bool = False # override the -iostore commandline option to not run it
    stage                   : bool = False # put this build in a stage directory
    skipstage               : bool = False # uses a stage directory, but assumes everything is already there, implies -stage
    manifests               : bool = False # generate streaming install manifests when cooking data
    createchunkinstall      : bool = False # generate streaming install data from manifest when cooking data, requires -stage & -manifests
    skipencryption          : bool = False # skips encrypting pak files even if crypto keys are provided
    archive                 : bool = False # put this build in an archive directory
    build                   : bool = False # True if build step should be executed
    noxge                   : bool = False # True if XGE should NOT be used for building
    CookPartialgc           : bool = False # while cooking clean up packages as we are done with them rather then cleaning everything up when we run out of space
    CookInEditor            : bool = False # Did we cook in the editor instead of in UAT
    IgnoreCookErrors        : bool = False # Ignores cook errors and continues with packaging etc
    nodebuginfo             : bool = False # do not copy debug files to the stage
    separatedebuginfo       : bool = False # output debug info to a separate directory
    MapFile                 : bool = False # generates a *.map file
    nocleanstage            : bool = False # skip cleaning the stage directory
    run                     : bool = False # run the game after it is built (including server, if -server)
    cookonthefly            : bool = False # run the client with cooked data provided by cook on the fly server
    Cookontheflystreaming   : bool = False # run the client in streaming cook on the fly mode (don't cache files locally instead force reget from server each file load)
    fileserver              : bool = False # run the client with cooked data provided by UnrealFileServer
    dedicatedserver         : bool = False # build, cook and run both a client and a server (also -server)
    client                  : bool = False # build, cook and run a client and a server, uses client target configuration
    noclient                : bool = False # do not run the client, just run the server
    logwindow               : bool = False # create a log window for the client
    package                 : bool = False # package the project for the target platform
    skippackage             : bool = False # Skips packaging the project for the target platform
    distribution            : bool = False # package for distribution the project
    PackageEncryptionKeyFile: bool = False # Path to file containing encryption key to use in packaging
    prereqs                 : bool = False # stage prerequisites along with the project
    applocaldir             : bool = False # location of prerequisites for applocal deployment
    Prebuilt                : bool = False # this is a prebuilt cooked and packaged build
    AdditionalPackageOptions: bool = False # extra options to pass to the platform's packager
    deploy                  : bool = False # deploy the project for the target platform
    getfile                 : bool = False # download file from target after successful run
    IgnoreLightMapErrors    : bool = False # Whether Light Map errors should be treated as critical
    stagingdirectory        : Optional[str]     = None # Directory to copy the builds to, i.e. -stagingdirectory=C:/Stage
    unrealexe               : Optional[str]     = None # Name of the Unreal Editor executable, i.e. -unrealexe=UnrealEditor.exe
    archivedirectory        : Optional[str]     = None # Directory to archive the builds to, i.e. -archivedirectory=C:/Archive
    archivemetadata         : bool = False # Archive extra metadata files in addition to the build (e.g. build.properties)
    createappbundle         : bool = False # When archiving for Mac, set this to true to package it in a .app bundle instead of normal loose files
    iterativecooking        : bool = False # Uses the iterative cooking, command line: -iterativecooking or -iterate
    CookMapsOnly            : bool = False # Cook only maps this only affects usage of -cookall the flag
    CookAll                 : bool = False # Cook all the things in the content directory for this project
    SkipCookingEditorContent: bool = False # Skips content under /Engine/Editor when cooking
    FastCook                : bool = False # Uses fast cook path if supported by target
    cmdline                 : Optional[str]     = None # command line to put into the stage in UECSCommandLine.txt
    bundlename              : Optional[str]     = None # string to use as the bundle name when deploying to mobile device
    map                     : Optional[str]     = None # map to run the game with
    AdditionalServerMapParams: Optional[str]    = None # Additional server map params, i.e ?param=value
    device                  : bool = False # Devices to run the game on
    serverdevice            : bool = False # Device to run the server on
    skipserver              : bool = False # Skip starting the server
    numclients              : Optional[int]     = None # Start extra clients, n should be 2 or more
    addcmdline              : Optional[str]     = None # Additional command line arguments for the program
    servercmdline           : Optional[str]     = None # Additional command line arguments for the program
    clientcmdline           : Optional[str]     = None # Override command line arguments to pass to the client
    nullrhi                 : bool = False # add -nullrhi to the client commandlines
    fakeclient              : bool = False # adds ?fake to the server URL
    editortest              : bool = False # rather than running a client, run the editor instead
    RunAutomationTests      : bool = False # when running -editortest or a client, run all automation tests, not compatible with -server
    Crash                   : Optional[int]     = None # when running -editortest or a client, adds commands like debug crash, debug rendercrash, etc based on index
    deviceuser              : Optional[str]     = None # Linux username for unattended key genereation
    devicepass              : Optional[str]     = None # Linux password
    RunTimeoutSeconds       : Optional[float]   = None # timeout to wait after we lunch the game
    SpecifiedArchitecture   : Optional[str]     = None # Determine a specific Minimum OS
    UbtArgs                 : Optional[str]     = None # extra options to pass to ubt
    MapsToRebuildLightMaps  : Optional[str]     = None # List of maps that need light maps rebuilding
    MapsToRebuildHLODMaps   : Optional[str]     = None # List of maps that need HLOD rebuilding
    ForceMonolithic         : bool = False # Toggle to combined the result into one executable
    ForceDebugInfo          : bool = False # Forces debug info even in development builds
    ForceNonUnity           : bool = False # Toggle to disable the unity build system
    ForceUnity              : bool = False # Toggle to force enable the unity build system
    Licensee                : bool = False # If set, this build is being compiled by a licensee
    NoSign                  : bool = False # Skips signing of code/content files.

@dataclass
class BuildEditorArgs:
    """Builds the editor for the specified project. Example BuildEditor -project=QAGame.
    Note: Editor will only ever build for the current platform in a Development config and required tools will be included
    """
    notools: bool = False # Don't build any tools (UHT, ShaderCompiler, CrashReporter


@dataclass
class LocalizeArgs:
    """Updates the external localization data using the arguments provided."""
    UEProjectRoot                   : Optional[str]  = None # Optional root-path to the project we're gathering for (defaults to CmdEnv.LocalRoot if unset).",
    UEProjectDirectory              : Optional[str]  = None # Sub-path to the project we're gathering for (relative to UEProjectRoot).",
    UEProjectName                   : Optional[str]  = None # Optional name of the project we're gathering for (should match its .uproject file, eg QAGame).",
    LocalizationProjectNames        : Optional[str]  = None # Comma separated list of the projects to gather text from.",
    LocalizationBranch              : Optional[str]  = None # Optional suffix to use when uploading the new data to the localization provider.",
    LocalizationProvider            : Optional[str]  = None # Optional localization provide override."),
    LocalizationSteps               : Optional[str]  = None # Optional comma separated list of localization steps to perform [Download, Gather, Import, Export, Compile, GenerateReports, Upload] (default is all). Only valid for projects using a modular config.",
    IncludePlugins                  : bool = False # Optional flag to include plugins from within the given UEProjectDirectory as part of the gather. This may optionally specify a comma separated list of the specific plugins to gather (otherwise all plugins will be gathered).",
    ExcludePlugins                  : Optional[str]  = None # Optional comma separated list of plugins to exclude from the gather.",
    IncludePlatforms                : bool = False # Optional flag to include platforms from within the given UEProjectDirectory as part of the gather.",
    AdditionalCSCommandletArguments : Optional[str]  = None # Optional arguments to pass to the gather process.",
    ParallelGather                  : bool = False # Run the gather processes for a single batch in parallel rather than sequence.",
# fmt: on


class UAT(Command):
    """Runs Unreal Automation tool.

    Notes
    -----

    We recommend users to create their own command class that specialize its use to a single purpose.

    We try not to use UAT as it ends up calling the editor anyway.
    """

    name: str = "uat"

    @staticmethod
    def arguments(subparsers):
        """Defines UAT arguments"""
        uat_parser = subparsers.add_parser("uat", help="Run the UAT command line tool")

        uat_parser.add_argument(
            "command", type=str, choices=commands, help="UAT Command to execute"
        )
        uat_parser.add_argument(
            "configuration",
            type=str,
            choices=get_build_modes(),
            help="Build configuration",
        )
        uat_parser.add_arguments(LocalizeArgs, dest="localize")
        uat_parser.add_arguments(BuildEditorArgs, dest="build_editor")
        uat_parser.add_arguments(BuildCookRunArgs, dest="build_cook_run")
        uat_parser.add_arguments(UATArgs, dest="uat")

    @staticmethod
    def execute(args):
        """Execute the UAT command"""

        uat_cmd = vars(args).pop("command")

        args = command_builder(args)

        subprocess.run(
            [uat()] + [uat_cmd] + args,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )


COMMAND = UAT


def cook_arguments_testing():
    """Experimental UAT cook command"""
    return [
        "BuildCookRun",
        "-configuration=Development",
        "-unattended",
        "-utf8output",
        "-noP4",
        "-allmaps",
        "-build",
        "-cook",
        "-pak",
        "-stage",
        "-WarningsAsErrors",
    ]


def cook_arguments_shipping():
    """Experimental UAT command cook"""
    return [
        "BuildCookRun",
        # "-Help",
        "-configuration=Shipping",
        "-unattended",
        "-utf8output",
        "-noP4",
        "-allmaps",
        "-build",
        "-cook",  # Used cooked data
        "-stage",  # Only stagged bulds can be paked, puts the build in its own directory
        "-pak",
        "-manifests",  # Generate a manifest of all the cooked files
        # "-chunkinstalldirectory={chunkdir}"
        # "-createchunkinstall",  # Create a chunk install
        "-prereqs",
        "-package",
        "-distribution",
        # -skippackage
        # f"-archive={output}",
        # -archivedirectory=Path
        "-nodebuginfo",  # Remove debug info
        # "-separatedebuginfo", #
        # -numclients=n
        # Builds crash reporter
        "-CrashReporter",
        "-WarningsAsErrors",
        # -ForceMonolithic
        # -ForceDebugInfo
        # -ForceNonUnity
        # -ForceUnity
        # -logwindow
        # -noxge no XGE
        # -signed sign the packfile
        # -clean wipe intermediate folder
        # -targetplatform=PlatformName       target platform for building, cooking and deployment (also -Platform)
        # -dedicatedserver
        # -servertargetplatform=PlatformName target platform for building, cooking and deployment of the dedicated server (also -ServerPlatform)
        # -destsample
        # -foreigndest
    ]


def cook_arguments_scratch():
    """Experimental UAT cook command"""
    return [
        # Base
        # ====
        # "-Help",
        # "-Verbose",
        # "-VeryVerbose",
        # "-List",
        # "-Compile",
        # "-NoCompile",
        # CSCommands
        # ========
        "BuildCookRun",
        # "BuildPlugin",
        # "BuildServer",
        # "BuildGame",
        # "Localise",
        # "RunUnreal",
        # "RunLowLevelTests",
        # "TestGauntlet",
        # "RunEditorTests",
        # -LogCmds="loginit warning, logexit warning, logdatabase error"
        "-configuration=Development",
        # f"-archivedirectory={project_folder}/Cooked",
        # Options
        # =======
        "-unattended",
        "-utf8output",
        "-noP4",
        "-allmaps",
        # "-clientconfig=Shipping",
        # "-serverconfig=Shipping",
        # "-nodebuginfo",
        "-build",
        "-cook",
        "-pak",
        "-stage",
        "-prereqs",
        # "-archive",
        "-WarningsAsErrors",
    ]


cook_profiles = dict(test=cook_arguments_testing, shipping=cook_arguments_shipping)

# pylint: disable=too-many-locals
def execute_uat_cook(args, profiles):
    """Experimental UAT cook command"""
    import os
    import sys

    from uetools.conf import load_conf
    from uetools.format.base import popen_with_format
    from uetools.format.cooking import CookingFormatter

    name = args.name
    platform = args.platform
    output = args.output

    projects_folder = load_conf().get("project_path")
    project_folder = os.path.join(projects_folder, name)
    uproject = os.path.join(project_folder, f"{name}.uproject")

    if output is None:
        output = os.path.join(project_folder, "Saved", "Cooked")

    base = [
        f"-project={uproject}",
        f"-platform={platform}",
        f"-stagingdirectory={output}",
    ]
    args = profiles.get(args.profile, profiles.get("test"))() + base

    print(args)
    fmt = CookingFormatter(24)
    fmt.print_non_matching = True

    returncode = popen_with_format(fmt, [uat()] + args)

    fmt.summary()

    print(f"Subprocess terminated with (rc: {returncode})")

    if returncode != 0:
        sys.exit(returncode)


@staticmethod
def execute_uat_test(args):
    """UAT & Gauntlet lookt totally unusable"""
    import os

    from uetools.conf import load_conf

    # Gauntlet seems to simply be launching the editor
    name = args.name
    test = args.test

    projects_folder = load_conf().get("project_path")
    project_folder = os.path.join(projects_folder, name)
    uproject = os.path.join(project_folder, f"{name}.uproject")

    # """
    # Gauntlet.Automation:
    #     CleanDevices
    #     PublishUnrealAutomationTelemetry
    #     RunEditorTests
    #     RunUnreal
    #     RunUnrealTests
    #     TestGauntlet
    # """

    # Error: Test EditorTest.EditorTestNode threw an exception during launch. Skipping test. Ex: Unreal tests should use ApplyToConfig(Config, Role, OtherRoles)
    #    at Gauntlet.UnrealTestConfiguration.ApplyToConfig(UnrealAppConfig AppConfig) in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Unreal\Base\Gauntlet.UnrealTestConfiguration.cs:line 803
    #    at EditorTest.EditorTestConfig.ApplyToConfig(UnrealAppConfig AppConfig, UnrealSessionRole ConfigRole, IEnumerable`1 OtherRoles) in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Editor\RunEditorTests.cs:line 53
    #    at Gauntlet.UnrealBuildSource.CreateConfiguration(UnrealSessionRole Role, IEnumerable`1 OtherRoles) in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Unreal\BuildSource\Gauntlet.UnrealBuildSource.cs:line 519
    #    at Gauntlet.UnrealSession.LaunchSession() in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Unreal\Base\Gauntlet.UnrealSession.cs:line 667
    #    at Gauntlet.UnrealTestNode`1.StartTest(Int32 Pass, Int32 InNumPasses) in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Unreal\Base\Gauntlet.UnrealTestNode.cs:line 702
    #    at Gauntlet.TextExecutor.StartTest(TestExecutionInfo TestInfo, Int32 Pass, Int32 NumPasses) in E:\UnrealEngine\Engine\Source\Programs\AutomationTool\Gauntlet\Framework\Gauntlet.TestExecutor.cs:line 553
    # Error: Test EditorTest.EditorTestNode (Win64 Development EditorGame) failed to start
    # Test EditorTest.EditorTestNode (Win64 Development EditorGame) NotStarted
    cmd_args = [
        uat(),
        "RunEditorTests",
        f"-project={uproject}",
        f"-testname={test}",
    ]

    # ERROR: Unable to find type uetools in assemblies. Namespaces= System.Linq.Enumerable+SelectArrayIterator`2[System.String,System.String].
    #  (see E:\UnrealEngine\Engine\Programs\AutomationTool\Saved\Logs\Log.txt for full exception trace)
    cmd_args = [
        uat(),
        "RunUnreal",
        f"-project={uproject}",
        "-platform=Win64",
        "--configuration=Development",
        "-build=local",
        f"-test={args.test}",
        # f'-build={engine}',
        # f'-log={log_path}',
        # '-TestExit=Automation Test Queue Empty',
        # f'-ExecCmds=Automation RunTests {args.test}',
    ]

    # ERROR: Unable to find type uetools in assemblies. Namespaces= System.Linq.Enumerable+SelectArrayIterator`2[System.String,System.String].
    #  (see E:\UnrealEngine\Engine\Programs\AutomationTool\Saved\Logs\Log.txt for full exception trace)
    cmd_args = [
        uat(),
        "RunUnrealTests",
        f"-project={uproject}",
        # f"-platform=Win64",
        # f"--configuration=Development",
        "-build=local",
        f"-test={args.test}",
        # f'-build={engine}',
        # f'-log={log_path}',
        # '-TestExit=Automation Test Queue Empty',
        # f'-ExecCmds=Automation RunTests {args.test}',
    ]

    subprocess.run(
        cmd_args, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True
    )
