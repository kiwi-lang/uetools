import os
import sys

from uetools.command import Command
from uetools.conf import editor_cmd, load_conf
from uetools.format.base import popen_with_format
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
        tests = subparsers.add_parser(
            RunTests.name, help="Run Unreal Automation Test (UAT)"
        )
        tests.add_argument("name", type=str, help="Project name")
        tests.add_argument("map", type=str, help="map name")
        tests.add_argument(
            "tests", type=str, default="uetools", help="Test section to run"
        )

    @staticmethod
    def execute(args):
        RunTests.execute_editor(args)

    @staticmethod
    def execute_editor(args):
        """Run the tests using the editor"""
        name = args.name

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, name)
        uproject = os.path.join(project_folder, f"{name}.uproject")

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
            uproject,
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
            f'-ReportExportPath="{project_folder}/Saved/Automation/Report"',
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

        if returncode != 0:
            sys.exit(returncode)


COMMAND = RunTests
