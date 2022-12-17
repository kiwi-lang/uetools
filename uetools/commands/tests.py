import os
import sys
from dataclasses import dataclass

from simple_parsing import choice

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import (
    editor_cmd,
    find_project,
    get_build_modes,
    guess_platform,
    uat,
)
from uetools.core.run import popen_with_format
from uetools.format.tests import TestFormatter


class RunTests(Command):
    """Execute automated tests for a given project

    Examples
    --------

    .. code-block:: console

       # Runs all the tests that contains `RTSGame` in their names
       uecli tests RTSGame /Game/Maps/AbilityTest/AbilityTest RTSGame

       # Runs all the map tests that have a functional tests
       uecli tests RTSGame /Game/Maps/AbilityTest/AbilityTest Project.Functional


    Notes
    -----

    You should build your project first.
    """

    name: str = "tests"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, RunTests)
        parser.add_argument("name", type=str, help="Project name")
        parser.add_argument("map", type=str, help="map name")
        parser.add_argument(
            "tests", type=str, default="uetools", help="Test section to run"
        )

    @staticmethod
    def execute(args):
        RunTests.execute_editor(args)

    @staticmethod
    def execute_editor(args):
        """Run the tests using the editor"""
        project = find_project(args.name)
        folder = os.path.dirname(project)

        # Commands a separated by ;
        # RunTest Accept a single argument
        # This is buggy, if I do Runtests uetools; Runtests Project;
        # it get stuck in a loop but if I run them sequentially it works as expected
        cmd = "; ".join(f"RunTests {name}" for name in args.tests.split(","))

        # # E:\UnrealEngine\Engine\Source\Developer\AutomationController\Private\AutomationCommandline.cpp
        # Valid automation commands
        #   Automation StartRemoteSession <sessionid>
        #   Automation List
        #   Automation RunTests <test string>
        #   Automation RunAll
        #   Automation RunFilter <Engine|Smoke|Stress|Perf|Product|All>
        #   Automation SetFilter <filter name>
        #   Automation Quit

        args = [
            editor_cmd(),
            project,
            args.map,
            "-stdout",
            "-FullStdOutLogOutput",
            "-utf8output",
            "-Unattended",
            "-NullRHI",
            "-NoSplash",
            "-NoSound",
            "-NoPause",
            "-noP4",
            f'-ReportExportPath="{folder}/Saved/Automation/Report"',
            "-allmaps",
            "-WarningsAsErrors",
            # This will make UE quit sucessfully (i.e no error code)
            "-TestExit=Automation Test Queue Empty",
            # Quit will force the engine to quit with a error code
            # if a test failed
            f"-ExecCmds=Automation {cmd}; Quit",
        ]

        fmt = TestFormatter(24)
        fmt.print_non_matching = True

        returncode = popen_with_format(fmt, args)

        fmt.summary()

        print(f"Subprocess terminated with (rc: {returncode})")

        return returncode


@dataclass
class UATArguments:
    """Arguments for the UAT command"""

    project: str
    test: str
    run: str = choice(
        "RunEditorTests",
        "RunUnreal",
        "RunUnrealTests",
        "TestGauntlet",
        type=str,
        default="RunUnrealTests",
    )
    platform: str = choice(*get_build_modes(), type=str, default=guess_platform())
    configuration: str = choice(*get_build_modes(), type=str, default="Development")
    build: str = "local"


class RunTestsUAT(Command):
    """Execute automated tests for a given project using UAT

    Notes
    -----
    This does not work
    """

    name: str = "uat-tests"

    @staticmethod
    def arguments(subparsers):
        """Defines UAT testing arguments"""
        parser = newparser(subparsers, RunTestsUAT)
        parser.add_arguments(UATArguments, dest="cook")

    @staticmethod
    def execute(args):
        """Execute the UAT command"""
        args = args.cook
        uat_cmd = vars(args).pop("run")

        uat_args = command_builder(args)
        cmd = [uat()] + [uat_cmd] + uat_args

        print(" ".join(cmd))

        fmt = TestFormatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd)
        fmt.summary()
        return returncode


COMMANDS = RunTests
