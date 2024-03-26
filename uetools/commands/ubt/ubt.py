from __future__ import annotations

from dataclasses import dataclass
import os

from argklass.arguments import add_arguments, choice
from argklass.command import Command, newparser

from uetools.core.conf import (
    find_project,
    get_build_modes,
    get_build_platforms,
    ubt,
    engine_folder,
)
from uetools.core.options import projectfield
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder, tailf
from uetools.format.base import Formatter


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


TARGETS = [
    "UnrealHeaderTool",
    "ShaderCompileWorker",
    "UnrealPak",
]


class UBT(Command):
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

    name: str = "ubt"

    # fmt: off
    @dataclass
    class Arguments:
        target              : str # target
        project             : str = projectfield() # Path to the project, example: <project>.uproject
        mode                : str | None = choice(*modes, default="Build")  # Select tool mode. One of the following (default tool mode is "Build"):
        verbose             : bool = False  # Increase output verbosity
        veryverbose         : bool = False  # Increase output verbosity more
        log                 : str | None  = None  # Specify a log file location instead of the default Engine/Programs/UnrealBuildTool/Log.txt
        tracewrites         : bool = False  # Trace writes requested to the specified file
        timestamps          : bool = False  # Include timestamps in the log
        frommsbuild         : bool = False  # Format messages for msbuild
        progress            : bool = False  # Write progress messages in a format that can be parsed by other programs
        nomutex             : bool = False  # Allow more than one instance of the program to run at once
        waitmutex           : bool = False  # Wait for another instance to finish and then start, rather than aborting immediately
        remoteini           : bool = False  # Remote tool ini directory
        clean               : bool = False  # Clean build products. Equivalent to -Mode=Clean
        projectfiles        : bool = False  # Generate project files based on IDE preference. Equivalent to -Mode=GenerateProjectFiles
        projectfileformat   : str | None  = None  # Generate project files in specified format. May be used multiple times.
        makefile            : bool = False  # Generate Linux Makefile
        cmakefile           : bool = False  # Generate project files for CMake
        qmakefile           : bool = False  # Generate project files for QMake
        kdevelopfile        : bool = False  # Generate project files for KDevelop
        codelitefiles       : bool = False  # Generate project files for Codelite
        xcodeprojectfiles   : bool = False  # Generate project files for XCode
        eddieprojectfiles   : bool = False  # Generate project files for Eddie
        vscode              : bool = False  # Generate project files for Visual Studio Code
        vsmac               : bool = False  # Generate project files for Visual Studio Mac
        clion               : bool = False  # Generate project files for CLion
        rider               : bool = False  # Generate project files for Rider
    # fmt: on

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, UBT)
        parser.add_argument(
            "--platform",
            default="Win64",
            type=str,
            help="Platform to compile for",
            choices=get_build_platforms(),
        )
        parser.add_argument(
            "--profile",
            default="Development",
            type=str,
            help="Build profile",
            choices=get_build_modes(),
        )
        add_arguments(parser, UBT.Arguments)

    @staticmethod
    def execute(args):
        pargs = [
            ubt(),
            args.target,
            args.platform,
            args.profile,
        ]

        if args.project:
            project = find_project(vars(args).pop("project"))
            pargs.append(f"-Project={project}")

        pargs += command_builder(args)

        log = os.path.join(engine_folder(), "Programs", "UnrealBuildTool", "Log.txt")
        if args.log is not None:
            log = args.log

        if os.path.exists(log):
            os.remove(log)

        with tailf(log):
            fmt = Formatter()
            return popen_with_format(fmt, pargs)


COMMANDS = UBT
