from __future__ import annotations
from argparse import ArgumentParser, REMAINDER
from dataclasses import dataclass, field
from typing import List
import subprocess

from gamekit.conf import Command, ubt, get_build_platforms, get_build_modes


# -Help               :  Display this help.
# -Verbose            :  Increase output verbosity
# -VeryVerbose        :  Increase output verbosity more
# -Log                :  Specify a log file location instead of the default Engine/Programs/UnrealBuildTool/Log.txt
# -TraceWrites        :  Trace writes requested to the specified file
# -Timestamps         :  Include timestamps in the log
# -FromMsBuild        :  Format messages for msbuild
# -Progress           :  Write progress messages in a format that can be parsed by other programs
# -NoMutex            :  Allow more than one instance of the program to run at once
# -WaitMutex          :  Wait for another instance to finish and then start, rather than aborting immediately
# -RemoteIni          :  Remote tool ini directory
# -Mode=              :  Select tool mode. One of the following (default tool mode is "Build"):
#                         AggregateParsedTimingInfo, Analyze, Build, Clean, Deploy, Execute, GenerateClangDatabase,
#                         GenerateProjectFiles, IOSPostBuildSync, JsonExport, ParseMsvcTimingInfo, PVSGather,
#                         QueryTargets, SetupPlatforms, ValidatePlatforms, WriteDocumentation, WriteMetadata
# -Clean              :  Clean build products. Equivalent to -Mode=Clean
# -ProjectFiles       :  Generate project files based on IDE preference. Equivalent to -Mode=GenerateProjectFiles
# -ProjectFileFormat= :  Generate project files in specified format. May be used multiple times.
# -Makefile           :  Generate Linux Makefile
# -CMakefile          :  Generate project files for CMake
# -QMakefile          :  Generate project files for QMake
# -KDevelopfile       :  Generate project files for KDevelop
# -CodeliteFiles      :  Generate project files for Codelite
# -XCodeProjectFiles  :  Generate project files for XCode
# -EddieProjectFiles  :  Generate project files for Eddie
# -VSCode             :  Generate project files for Visual Studio Code
# -VSMac              :  Generate project files for Visual Studio Mac
# -CLion              :  Generate project files for CLion
# -Rider              :  Generate project files for Rider

TARGETS = [
    'UnrealHeaderTool',
    'ShaderCompileWorker',
    'UnrealPak',
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
        ubt_parser = subparsers.add_parser('ubt', help="")
        ubt_parser.add_argument("target", type=str, help="target name")
        ubt_parser.add_argument("--project", default=None, type=str, help="Path to the project, example: <project>.uproject")
        ubt_parser.add_argument("--platform", default='Win64', type=str, help="Platofrm to compile for", choices=get_build_platforms())
        ubt_parser.add_argument("--profile", default='Development', type=str, help="Build profile", choices=get_build_modes())
        ubt_parser.add_argument("--log", type=str, help="Path to log file")

    @staticmethod
    def execute(args):
        pargs = [
                ubt(),
                args.target,
                args.platform,
                args.profile,
        ]

        if args.project:
            pargs.append(f'-Project={args.project}')

        if args.log:
            pargs.append(f'-log={args.log}')

        p = subprocess.run(
            pargs,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True
        )

        print(f"Subprocess terminated with (rc: {p.returncode})")
        return

COMMAND = UBT
