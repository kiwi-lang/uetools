from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass
from typing import Optional

from simple_parsing import choice

from uetools.command import Command, command_builder
from uetools.conf import get_build_modes, get_build_platforms, ubt

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
    """Unreal Build tools arguments"""
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
        ubt_parser = subparsers.add_parser("ubt", help="")
        ubt_parser.add_argument("target", type=str, help="target name")
        ubt_parser.add_argument(
            "--project",
            default=None,
            type=str,
            help="Path to the project, example: <project>.uproject",
        )
        ubt_parser.add_argument(
            "--platform",
            default="Win64",
            type=str,
            help="Platofrm to compile for",
            choices=get_build_platforms(),
        )
        ubt_parser.add_argument(
            "--profile",
            default="Development",
            type=str,
            help="Build profile",
            choices=get_build_modes(),
        )
        ubt_parser.add_arguments(Arguments, dest="args")

    @staticmethod
    def execute(args):
        pargs = [
            ubt(),
            args.target,
            args.platform,
            args.profile,
        ]

        if args.project:
            pargs.append(f"-Project={args.project}")

        pargs += command_builder(asdict(args.args))

        subprocess.run(
            pargs, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True
        )


COMMAND = UBT
