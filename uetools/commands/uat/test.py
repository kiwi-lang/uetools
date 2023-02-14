from dataclasses import dataclass

from uetools.core.arguments import add_arguments, choice
from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import get_build_modes, guess_platform, uat
from uetools.core.run import popen_with_format
from uetools.format.tests import TestFormatter


def commands():
    return choice(
        "RunEditorTests",
        "RunUnreal",
        "RunUnrealTests",
        "TestGauntlet",
        type=str,
        default="RunUnrealTests",
    )


@dataclass
class UATArguments:
    """Arguments for the UAT command"""

    project: str
    test: str
    run: str = commands()
    platform: str = choice(*get_build_modes(), type=str, default=guess_platform())
    configuration: str = choice(*get_build_modes(), type=str, default="Development")
    build: str = "local"


class RunTestsUAT(Command):
    """Execute automated tests for a given project using UAT

    Notes
    -----
    This does not work
    """

    name: str = "test"

    @staticmethod
    def arguments(subparsers):
        """Defines UAT testing arguments"""
        parser = newparser(subparsers, RunTestsUAT)
        add_arguments(parser, UATArguments)

    @staticmethod
    def execute(args):
        """Execute the UAT command"""
        uat_cmd = vars(args).pop("run")

        uat_args = command_builder(args)
        cmd = [uat()] + [uat_cmd] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = TestFormatter(24)
        fmt.print_non_matching = True
        returncode = popen_with_format(fmt, cmd)
        fmt.summary()
        return returncode


COMMANDS = RunTestsUAT
