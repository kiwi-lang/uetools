from __future__ import annotations

import subprocess
from argparse import REMAINDER, ArgumentParser
from dataclasses import dataclass, field
from typing import List

from uetools.conf import Command, uat


@dataclass
class Flag:
    """A boolean flag"""

    name: str
    help: str


@dataclass
class Map:
    """A mapping"""

    name: str
    help: str


@dataclass
class CSCommand:
    """A command with arguments"""

    name: str
    help: str = ""
    flags: List[Flag] = field(default_factory=list)
    commands: List[CSCommand] = field(default_factory=list)


UATArgs = CSCommand(
    "UAT",
    "Unreal Automation tools",
    [
        Flag("-Verbose", help="Enables verbose logging"),
        Flag("-VeryVerbose", help="Enables very verbose logging"),
        Flag("-Submit", help="Allows UAT command to submit changes"),
        Flag("-NoSubmit", help="Prevents any submit attempts"),
        Flag(
            "-NoP4",
            help="Disables Perforce functionality {default if not run on a build machine}",
        ),
        Flag(
            "-P4",
            help="Enables Perforce functionality {default if run on a build machine}",
        ),
        Flag("-Help", help="Displays help"),
        Flag("-List", help="Lists all available commands"),
        Flag("-NoKill", help="Does not kill any spawned processes on exit"),
        Flag("-Compile", help="Force all script modules to be compiled"),
        Flag(
            "-NoCompile",
            help="Do not attempt to compile any script modules - attempts to run with whatever is up to date",
        ),
        Flag(
            "-IgnoreBuildRecords",
            help="Ignore build records (Intermediate/ScriptModule/ProjectName.json) files when determining if script modules are up to date",
        ),
        Flag(
            "-UseLocalBuildStorage",
            help="Allows you to use local storage for your root build storage dir {default of P:/Builds {on PC} is changed to Engine/Saved/LocalBuilds}. Used for local testing.",
        ),
        Flag(
            "-WaitForDebugger",
            help="Waits for a debugger to be attached, and breaks once debugger successfully attached.",
        ),
    ],
    [
        CSCommand("AnalyzeThirdPartyLibs"),
        CSCommand("BenchmarkBuild"),
        CSCommand("BenchmarkOptions"),
        CSCommand("BuildCMakeLib"),
        CSCommand("BuildCommonTools"),
        CSCommand(
            "BuildCookRun",
            "",
            [
                Flag(
                    "-project=Path",
                    "Project path (required), i.e: -project=QAGame, -project=Samples/BlackJack/BlackJack.uproject, -project=D:/Projects/MyProject.uproject",
                ),
                Flag("-destsample", "Destination Sample name"),
                Flag("-foreigndest", "Foreign Destination"),
                Flag(
                    "-targetplatform=PlatformName",
                    "target platform for building, cooking and deployment (also -Platform)",
                ),
                Flag(
                    "-servertargetplatform=PlatformName",
                    "target platform for building, cooking and deployment of the dedicated server (also -ServerPlatform)",
                ),
                Flag(
                    "-foreign",
                    "Generate a foreign uproject from blankproject and use that",
                ),
                Flag(
                    "-foreigncode",
                    "Generate a foreign code uproject from platformergame and use that",
                ),
                Flag("-CrashReporter", "true if we should build crash reporter"),
                Flag(
                    "-cook",
                    "-cookonthefly Determines if the build is going to use cooked data",
                ),
                Flag(
                    "-skipcook",
                    "use a cooked build, but we assume the cooked data is up to date and where it belongs, implies -cook",
                ),
                Flag(
                    "-skipcookonthefly",
                    "in a cookonthefly build, used solely to pass information to the package step",
                ),
                Flag("-clean", "wipe intermediate folders before building"),
                Flag(
                    "-unattended",
                    "assumes no operator is present, always terminates without waiting for something.",
                ),
                Flag("-pak", "generate a pak file"),
                Flag("-iostore", "generate I/O store container file(s)"),
                Flag("-cook4iostore", "generate I/O store container file(s)"),
                Flag("-zenstore", "save cooked output data to the Zen storage server"),
                Flag(
                    "-makebinaryconfig",
                    "generate optimized config data during staging to improve loadtimes",
                ),
                Flag(
                    "-signpak=keys",
                    "sign the generated pak file with the specified key, i.e. -signpak=C:/Encryption.keys. Also implies -signedpak.",
                ),
                Flag(
                    "-prepak",
                    "attempt to avoid cooking and instead pull pak files from the network, implies pak and skipcook",
                ),
                Flag("-signed", "the game should expect to use a signed pak file."),
                Flag(
                    "-PakAlignForMemoryMapping",
                    "The game will be set up for memory mapping bulk data.",
                ),
                Flag(
                    "-skippak",
                    "use a pak file, but assume it is already built, implies pak",
                ),
                Flag(
                    "-skipiostore",
                    "override the -iostore commandline option to not run it",
                ),
                Flag("-stage", "put this build in a stage directory"),
                Flag(
                    "-skipstage",
                    "uses a stage directory, but assumes everything is already there, implies -stage",
                ),
                Flag(
                    "-manifests",
                    "generate streaming install manifests when cooking data",
                ),
                Flag(
                    "-createchunkinstall",
                    "generate streaming install data from manifest when cooking data, requires -stage & -manifests",
                ),
                Flag(
                    "-skipencryption",
                    "skips encrypting pak files even if crypto keys are provided",
                ),
                Flag("-archive", "put this build in an archive directory"),
                Flag("-build", "True if build step should be executed"),
                Flag("-noxge", "True if XGE should NOT be used for building"),
                Flag(
                    "-CookPartialgc",
                    "while cooking clean up packages as we are done with them rather then cleaning everything up when we run out of space",
                ),
                Flag("-CookInEditor", "Did we cook in the editor instead of in UAT"),
                Flag(
                    "-IgnoreCookErrors",
                    "Ignores cook errors and continues with packaging etc",
                ),
                Flag("-nodebuginfo", "do not copy debug files to the stage"),
                Flag("-separatedebuginfo", "output debug info to a separate directory"),
                Flag("-MapFile", "generates a *.map file"),
                Flag("-nocleanstage", "skip cleaning the stage directory"),
                Flag(
                    "-run",
                    "run the game after it is built (including server, if -server)",
                ),
                Flag(
                    "-cookonthefly",
                    "run the client with cooked data provided by cook on the fly server",
                ),
                Flag(
                    "-Cookontheflystreaming",
                    "run the client in streaming cook on the fly mode (don't cache files locally instead force reget from server each file load)",
                ),
                Flag(
                    "-fileserver",
                    "run the client with cooked data provided by UnrealFileServer",
                ),
                Flag(
                    "-dedicatedserver",
                    "build, cook and run both a client and a server (also -server)",
                ),
                Flag(
                    "-client",
                    "build, cook and run a client and a server, uses client target configuration",
                ),
                Flag("-noclient", "do not run the client, just run the server"),
                Flag("-logwindow", "create a log window for the client"),
                Flag("-package", "package the project for the target platform"),
                Flag(
                    "-skippackage",
                    "Skips packaging the project for the target platform",
                ),
                Flag("-distribution", "package for distribution the project"),
                Flag(
                    "-PackageEncryptionKeyFile",
                    "Path to file containing encryption key to use in packaging",
                ),
                Flag("-prereqs", "stage prerequisites along with the project"),
                Flag(
                    "-applocaldir", "location of prerequisites for applocal deployment"
                ),
                Flag("-Prebuilt", "this is a prebuilt cooked and packaged build"),
                Flag(
                    "-AdditionalPackageOptions",
                    "extra options to pass to the platform's packager",
                ),
                Flag("-deploy", "deploy the project for the target platform"),
                Flag("-getfile", "download file from target after successful run"),
                Flag(
                    "-IgnoreLightMapErrors",
                    "Whether Light Map errors should be treated as critical",
                ),
                Flag(
                    "-stagingdirectory=Path",
                    "Directory to copy the builds to, i.e. -stagingdirectory=C:/Stage",
                ),
                Flag(
                    "-unrealexe=ExecutableName",
                    "Name of the Unreal Editor executable, i.e. -unrealexe=UnrealEditor.exe",
                ),
                Flag(
                    "-archivedirectory=Path",
                    "Directory to archive the builds to, i.e. -archivedirectory=C:/Archive",
                ),
                Flag(
                    "-archivemetadata",
                    "Archive extra metadata files in addition to the build (e.g. build.properties)",
                ),
                Flag(
                    "-createappbundle",
                    "When archiving for Mac, set this to true to package it in a .app bundle instead of normal loose files",
                ),
                Flag(
                    "-iterativecooking",
                    "Uses the iterative cooking, command line: -iterativecooking or -iterate",
                ),
                Flag(
                    "-CookMapsOnly",
                    "Cook only maps this only affects usage of -cookall the flag",
                ),
                Flag(
                    "-CookAll",
                    "Cook all the things in the content directory for this project",
                ),
                Flag(
                    "-SkipCookingEditorContent",
                    "Skips content under /Engine/Editor when cooking",
                ),
                Flag("-FastCook", "Uses fast cook path if supported by target"),
                Flag(
                    "-cmdline",
                    "command line to put into the stage in UECSCommandLine.txt",
                ),
                Flag(
                    "-bundlename",
                    "string to use as the bundle name when deploying to mobile device",
                ),
                Flag("-map", "map to run the game with"),
                Flag(
                    "-AdditionalServerMapParams",
                    "Additional server map params, i.e ?param=value",
                ),
                Flag("-device", "Devices to run the game on"),
                Flag("-serverdevice", "Device to run the server on"),
                Flag("-skipserver", "Skip starting the server"),
                Flag("-numclients=n", "Start extra clients, n should be 2 or more"),
                Flag(
                    "-addcmdline", "Additional command line arguments for the program"
                ),
                Flag(
                    "-servercmdline",
                    "Additional command line arguments for the program",
                ),
                Flag(
                    "-clientcmdline",
                    "Override command line arguments to pass to the client",
                ),
                Flag("-nullrhi", "add -nullrhi to the client commandlines"),
                Flag("-fakeclient", "adds ?fake to the server URL"),
                Flag(
                    "-editortest",
                    "rather than running a client, run the editor instead",
                ),
                Flag(
                    "-RunAutomationTests",
                    "when running -editortest or a client, run all automation tests, not compatible with -server",
                ),
                Flag(
                    "-Crash=index",
                    "when running -editortest or a client, adds commands like debug crash, debug rendercrash, etc based on index",
                ),
                Flag("-deviceuser", "Linux username for unattended key genereation"),
                Flag("-devicepass", "Linux password"),
                Flag("-RunTimeoutSeconds", "timeout to wait after we lunch the game"),
                Flag("-SpecifiedArchitecture", "Determine a specific Minimum OS"),
                Flag("-UbtArgs", "extra options to pass to ubt"),
                Flag(
                    "-MapsToRebuildLightMaps",
                    "List of maps that need light maps rebuilding",
                ),
                Flag(
                    "-MapsToRebuildHLODMaps", "List of maps that need HLOD rebuilding"
                ),
                Flag(
                    "-ForceMonolithic",
                    "Toggle to combined the result into one executable",
                ),
                Flag("-ForceDebugInfo", "Forces debug info even in development builds"),
                Flag("-ForceNonUnity", "Toggle to disable the unity build system"),
                Flag("-ForceUnity", "Toggle to force enable the unity build system"),
                Flag("-Licensee", "If set, this build is being compiled by a licensee"),
                Flag("-NoSign", "Skips signing of code/content files."),
            ],
        ),
        CSCommand("BuildDerivedDataCache"),
        CSCommand(
            "BuildEditor",
            "Builds the editor for the specified project. Example BuildEditor -project=QAGame. Note: Editor will only ever build for the current platform in a Development config and required tools will be included",
            [
                Map(
                    "-project",
                    "Project to build. Will search current path and paths in ueprojectdirs. If omitted will build vanilla UnrealEditor",
                ),
                Flag(
                    "-notools",
                    "Don't build any tools (UHT, ShaderCompiler, CrashReporter",
                ),
            ],
        ),
        CSCommand("BuildGame"),
        CSCommand("BuildHlslcc"),
        CSCommand("BuildPhysX"),
        CSCommand("BuildPlugin"),
        CSCommand("BuildServer"),
        CSCommand("BuildTarget"),
        CSCommand("BuildThirdPartyLibs"),
        CSCommand("CheckBalancedMacros"),
        CSCommand("CheckCsprojDotNetVersion"),
        CSCommand("CheckForHacks"),
        CSCommand("CheckPerforceCase"),
        CSCommand("CheckRestrictedFolders"),
        CSCommand("CheckTargetExists"),
        CSCommand("CheckXcodeVersion"),
        CSCommand("CleanAutomationReports"),
        CSCommand("CleanFormalBuilds"),
        CSCommand("CopySharedCookedBuild"),
        CSCommand("CopyUAT"),
        CSCommand("CreateComponentZips"),
        CSCommand("CreatePlatformExtension"),
        CSCommand("CryptoKeys"),
        CSCommand("DownloadJupiterBuild"),
        CSCommand("ExportMcpTemplates"),
        CSCommand("ExtractPaks"),
        CSCommand("FinalizeInstalledBuild"),
        CSCommand("FixPerforceCase"),
        CSCommand("FixupRedirects"),
        CSCommand("GenerateDSYM"),
        CSCommand("GeneratePlatformReport"),
        CSCommand("IPhonePackager"),
        CSCommand("ListMobileDevices"),
        CSCommand("ListThirdPartySoftware"),
        # no doc
        # CSCommand('Localise'),
        CSCommand(
            "Localize",
            "Updates the external localization data using the arguments provided.",
            [
                Flag(
                    "-UEProjectRoot",
                    "Optional root-path to the project we're gathering for (defaults to CmdEnv.LocalRoot if unset).",
                ),
                Flag(
                    "-UEProjectDirectory",
                    "Sub-path to the project we're gathering for (relative to UEProjectRoot).",
                ),
                Flag(
                    "-UEProjectName",
                    "Optional name of the project we're gathering for (should match its .uproject file, eg QAGame).",
                ),
                Flag(
                    "-LocalizationProjectNames",
                    "Comma separated list of the projects to gather text from.",
                ),
                Flag(
                    "-LocalizationBranch",
                    "Optional suffix to use when uploading the new data to the localization provider.",
                ),
                Flag(
                    "-LocalizationProvider", "Optional localization provide override."
                ),
                Flag(
                    "-LocalizationSteps",
                    "Optional comma separated list of localization steps to perform [Download, Gather, Import, Export, Compile, GenerateReports, Upload] (default is all). Only valid for projects using a modular config.",
                ),
                Flag(
                    "-IncludePlugins",
                    "Optional flag to include plugins from within the given UEProjectDirectory as part of the gather. This may optionally specify a comma separated list of the specific plugins to gather (otherwise all plugins will be gathered).",
                ),
                Flag(
                    "-ExcludePlugins",
                    "Optional comma separated list of plugins to exclude from the gather.",
                ),
                Flag(
                    "-IncludePlatforms",
                    "Optional flag to include platforms from within the given UEProjectDirectory as part of the gather.",
                ),
                Flag(
                    "-AdditionalCSCommandletArguments",
                    "Optional arguments to pass to the gather process.",
                ),
                Flag(
                    "-ParallelGather",
                    "Run the gather processes for a single batch in parallel rather than sequence.",
                ),
            ],
        ),
        CSCommand("MegaXGE"),
        CSCommand("MemreportHelper"),
        CSCommand("OpenEditor"),
        CSCommand("ParseMsvcTimingInfo"),
        CSCommand("RebuildHLOD"),
        CSCommand("RebuildLightMaps"),
        CSCommand("RecordPerformance"),
        CSCommand("ReplaceAssetsUsingManifest"),
        CSCommand("ResavePackages"),
        CSCommand("StashTarget"),
        CSCommand("SyncBinariesFromUGS"),
        CSCommand("SyncDDC"),
        CSCommand("SyncDepotPath"),
        CSCommand("SyncProject"),
        CSCommand("UnrealBuildUtilDummyBuildCSCommand"),
        CSCommand("UnstashTarget"),
        CSCommand("UpdateLocalVersion"),
        CSCommand("UploadDDCToAWS"),
        CSCommand("WorldPartitionBuilder"),
        CSCommand("ZipProjectUp"),
        CSCommand("ZipUtils"),
        CSCommand("P4WriteConfig"),
        CSCommand("Build"),
        CSCommand("BuildGraph"),
        CSCommand("CleanTempStorage"),
        CSCommand("TempStorageTests"),
        CSCommand("MakeCookedEditor"),
        CSCommand("CleanDevices"),
        CSCommand("PublishUnrealAutomationTelemetry"),
        CSCommand("RunEditorTests"),
        CSCommand("ExportIPAFromArchive"),
        CSCommand("MakeIPA"),
        CSCommand("WriteIniValueToPlist"),
        # No doc
        # CSCommand('RunLowLevelTests'),
        # CSCommand('TestGauntlet'),
        # CSCommand('RunUnrealTests'),
        # CSCommand('RunUnreal'),
        CSCommand("Turnkey"),
    ],
)


commands = {}


class UAT(Command):
    """Runs uat as is. Experimental do not use


    Notes
    -----

    We try not to use UAT as it ends up calling the Editor anyway.
    """

    name: str = "uat"

    @staticmethod
    def arguments(subparsers):
        """Defines UAT arguments"""
        uat_parser = subparsers.add_parser("uat", help=UATArgs.help)

        for flag in UATArgs.flags:
            uat_parser.add_argument(flag.name, action="store_true", help=flag.help)

        for cmd in UATArgs.commands:
            cmd_parser = ArgumentParser(cmd.name, description=cmd.help)

            for flag in cmd.flags:
                cmd_parser.add_argument(flag.name, action="store_true", help=flag.help)

            commands[cmd.name] = (cmd_parser, cmd)

        uat_parser.add_argument("exec", choices=list(commands.keys()))
        uat_parser.add_argument("args", nargs=REMAINDER)

    @staticmethod
    def execute(args):
        """Execute the UAT command"""
        cmd = args.exec

        cmd_parser = commands.get(cmd, [None, None])[0]
        if cmd_parser is None:
            print(f"Unsupported command {cmd}")
            return

        cmd_args = cmd_parser.parse_args(args.args)

        ue_args = []

        for k, v in vars(args).items():
            if v and k not in ("exec", "command"):
                ue_args.append(f"-{k}")

        ue_args.append(cmd)

        for k, v in vars(cmd_args).items():
            if v:
                ue_args.append(f"-{k}")

        subprocess.run(
            [uat()] + ue_args,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        return


COMMAND = UAT

#
# Different UAT CSCommands
#


"""

Executes scripted commands


AutomationTool.exe [-verbose] [-compileonly] [-p4] CSCommand0 [-Arg0 -Arg1 -Arg2 ...] CSCommand1 [-Arg0 -Arg1 ...] CSCommand2 [-Arg0 ...] CSCommandn ... [EnvVar0=MyValue0 ... EnvVarn=MyValuen]

Parameters:
    -Verbose                 Enables verbose logging
    -VeryVerbose             Enables very verbose logging
    -Submit                  Allows UAT command to submit changes
    -NoSubmit                Prevents any submit attempts
    -NoP4                    Disables Perforce functionality {default if not run on a build machine}
    -P4                      Enables Perforce functionality {default if run on a build machine}
    -Help                    Displays help
    -List                    Lists all available commands
    -NoKill                  Does not kill any spawned processes on exit
    -Compile                 Force all script modules to be compiled
    -NoCompile               Do not attempt to compile any script modules - attempts to run with whatever is up to date
    -IgnoreBuildRecords      Ignore build records (Intermediate/ScriptModule/ProjectName.json) files when determining if script modules are up to date
    -UseLocalBuildStorage    Allows you to use local storage for your root build storage dir {default of P:/Builds {on PC} is changed to Engine/Saved/LocalBuilds}. Used for local testing.
    -WaitForDebugger         Waits for a debugger to be attached, and breaks once debugger successfully attached.

"""


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

    from uetools.commands.fmt import CookingFormater, popen_with_format
    from uetools.conf import load_conf

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
    fmt = CookingFormater(24)
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
