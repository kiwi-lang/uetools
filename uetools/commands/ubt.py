from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from simple_parsing import choice

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import find_project, get_build_modes, get_build_platforms, ubt
from uetools.core.run import run

modes = [
    "AggregateParsedTimingInfo",
    "Analyze",
    "Build",
    "Clean",
    "Deploy",
    "Execute",
    "GenerateClangDatabase",
    "GenerateProjectFiles",
    "IOSPostBuildSync",
    "JsonExport",
    "ParseMsvcTimingInfo",
    "PVSGather",
    "QueryTargets",
    "SetupPlatforms",
    "ValidatePlatforms",
    "WriteDocumentation",
    "WriteMetadata",
]


# fmt: off
@dataclass
class Arguments:
    """Unreal Build tools arguments

    Attributes
    ----------
    mode, str
        Select tool mode. One of the following (default tool mode is "Build"):
    verbose, bool
        Increase output verbosity
    veryverbose, bool
        Increase output verbosity more
    log, str
        Specify a log file location instead of the default Engine/Programs/UnrealBuildTool/Log.txt
    tracewrites, str
        Trace writes requested to the specified file
    timestamps, bool
        Include timestamps in the log
    frommsbuild, bool
        Format messages for msbuild
    progress, bool
        Write progress messages in a format that can be parsed by other programs
    nomutex, bool
        Allow more than one instance of the program to run at once
    waitmutex, bool
        Wait for another instance to finish and then start, rather than aborting immediately
    remoteini, str
        Remote tool ini directory
    clean, bool
        Clean build products. Equivalent to -Mode=Clean
    projectfiles, bool
        Generate project files based on IDE preference. Equivalent to -Mode=GenerateProjectFiles
    projectfileformat, str
        Generate project files in specified format. May be used multiple times.
    makefile, bool
        Generate Linux Makefile
    cmakefile, bool
        Generate project files for CMake
    qmakefile, bool
        Generate project files for QMake
    kdevelopfile, bool
        Generate project files for KDevelop
    codelitefiles, bool
        Generate project files for Codelite
    xcodeprojectfiles, bool
        Generate project files for XCode
    eddieprojectfiles, bool
        Generate project files for Eddie
    vscode, bool
        Generate project files for Visual Studio Code
    vsmac, bool
        Generate project files for Visual Studio Mac
    clion, bool
        Generate project files for CLion
    rider, bool
        Generate project files for Rider

    """
    mode                : Optional[str] = choice(*modes, default="Build")  #   Select tool mode. One of the following (default tool mode is "Build"):
    verbose             : bool = False  #   Increase output verbosity
    veryverbose         : bool = False  #   Increase output verbosity more
    log                 : Optional[str]  = None  #   Specify a log file location instead of the default Engine/Programs/UnrealBuildTool/Log.txt
    tracewrites         : bool = False  #   Trace writes requested to the specified file
    timestamps          : bool = False  #   Include timestamps in the log
    frommsbuild         : bool = False  #   Format messages for msbuild
    progress            : bool = False  #   Write progress messages in a format that can be parsed by other programs
    nomutex             : bool = False  #   Allow more than one instance of the program to run at once
    waitmutex           : bool = False  #   Wait for another instance to finish and then start, rather than aborting immediately
    remoteini           : bool = False  #   Remote tool ini directory
    clean               : bool = False  #   Clean build products. Equivalent to -Mode=Clean
    projectfiles        : bool = False  #   Generate project files based on IDE preference. Equivalent to -Mode=GenerateProjectFiles
    projectfileformat   : Optional[str]  = None  #   Generate project files in specified format. May be used multiple times.
    makefile            : bool = False  #   Generate Linux Makefile
    cmakefile           : bool = False  #   Generate project files for CMake
    qmakefile           : bool = False  #   Generate project files for QMake
    kdevelopfile        : bool = False  #   Generate project files for KDevelop
    codelitefiles       : bool = False  #   Generate project files for Codelite
    xcodeprojectfiles   : bool = False  #   Generate project files for XCode
    eddieprojectfiles   : bool = False  #   Generate project files for Eddie
    vscode              : bool = False  #   Generate project files for Visual Studio Code
    vsmac               : bool = False  #   Generate project files for Visual Studio Mac
    clion               : bool = False  #   Generate project files for CLion
    rider               : bool = False  #   Generate project files for Rider
# fmt: on

TARGETS = [
    "UnrealHeaderTool",
    "ShaderCompileWorker",
    "UnrealPak",
]


class UBT(Command):
    """Runs Unreal build tool as is.

    Notes
    -----
    Experimental do not use

    """

    name: str = "ubt"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, UBT)
        parser.add_argument("target", type=str, help="target name")
        parser.add_argument(
            "--project",
            default=None,
            type=str,
            help="Path to the project, example: <project>.uproject",
        )
        parser.add_argument(
            "--platform",
            default="Win64",
            type=str,
            help="Platofrm to compile for",
            choices=get_build_platforms(),
        )
        parser.add_argument(
            "--profile",
            default="Development",
            type=str,
            help="Build profile",
            choices=get_build_modes(),
        )
        parser.add_arguments(Arguments, dest="args")

    @staticmethod
    def execute(args):
        pargs = [
            ubt(),
            args.target,
            args.platform,
            args.profile,
        ]

        if args.project:
            project = find_project(args.project)
            pargs.append(f"-Project={project}")

        pargs += command_builder(asdict(args.args))

        run(pargs, check=True)


COMMANDS = UBT
