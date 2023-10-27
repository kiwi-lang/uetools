import os
from dataclasses import dataclass

from argklass.command import Command

from uetools.core.conf import editor_cmd, find_project
from uetools.core.options import projectfield
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

    name: str = "run"

    @dataclass
    class Arguments:
        # fmt: off
        map         : str                               # map name
        tests       : str           = "uetools"         # Test section to run
        project     : str           = projectfield()  # Name of the project to modify.
        # fmt: on

    @staticmethod
    def execute(args):
        RunTests.execute_editor(args)

    @staticmethod
    def execute_editor(args):
        """Run the tests using the editor"""
        project = find_project(args.project)
        folder = os.path.dirname(project)

        # Commands a separated by ;
        # RunTest Accept a single argument
        # This is buggy, if I do Runtests uetools; Runtests Project;
        # it get stuck in a loop but if I run them sequentially it works as expected
        cmd = "; ".join(f"RunTests {name}" for name in args.tests.split(","))

        # # E:\UnrealEngine\Engine\Source\Developer\AutomationController\Private\AutomationCommandline.cpp
        # Valid automation commands
        #  Automation StartRemoteSession <sessionid>
        #  Automation List
        #  Automation RunTests <test string>
        #  Automation RunAll
        #  Automation RunFilter <Engine|Smoke|Stress|Perf|Product|All>
        #  Automation SetFilter <filter name>
        #  Automation Quit

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
            # "-abslog=E:/uetools/tests/format/samples/tests_in.txt",
            "-NoSound",
            "-NoPause",
            "-noP4",
            f'-ReportExportPath="{folder}/Saved/Automation/Report"',
            "-allmaps",
            "-WarningsAsErrors",
            # This will make UE quit successfully (i.e no error code)
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


COMMANDS = RunTests
